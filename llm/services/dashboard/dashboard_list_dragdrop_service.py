import json
import os
from typing import Annotated, List, Dict
from fastapi import Depends, HTTPException
from core.store_to_r2 import R2ObjectStorage
from schemas.dashboard_schema import (
    ListDragDropLayoutSchema,
    ListDragDropRequestSchema,
    ListDragDropResponseSchema,
    ListComponentLayout,
    ListColumn,
    ListPosition,
    Layout,
)
import re
from bs4 import BeautifulSoup


class DashboardListDragDropService:
    """Service for handling list-based drag-and-drop layout modifications."""

    def __init__(
        self,
        r2: Annotated[
            R2ObjectStorage,
            Depends(
                lambda: R2ObjectStorage(
                    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev"
                )
            ),
        ],
    ):
        self.r2 = r2

    def extract_components_from_layout(self, layout: Layout) -> tuple[List[ListComponentLayout], List[ListColumn]]:
        """Extract components from HTML layout and organize them into columns."""
        components = []
        
        # Parse HTML to find components
        soup = BeautifulSoup(layout.html, 'html.parser')
        
        # Find all potential components
        component_elements = soup.find_all(['div', 'canvas', 'table', 'section'], 
                                         class_=lambda x: x and ('chart' in x.lower() or 
                                                                'table' in x.lower() or 
                                                                'component' in x.lower()))
        
        # If no specific components found, find all div elements
        if not component_elements:
            component_elements = soup.find_all('div')
        
        # Create default columns
        columns = [
            ListColumn(
                column_id="col-main",
                title="Main Components",
                width=4,
                component_ids=[]
            ),
            ListColumn(
                column_id="col-secondary",
                title="Secondary Components",
                width=4,
                component_ids=[]
            ),
            ListColumn(
                column_id="col-sidebar",
                title="Sidebar Components",
                width=4,
                component_ids=[]
            )
        ]
        
        # Distribute components across columns
        for i, element in enumerate(component_elements[:15]):  # Limit to 15 components
            component_id = element.get('id', f'list-component-{i}')
            component_type = self._determine_component_type(element)
            
            # Determine which column to place the component in
            if component_type in ['chart', 'table']:
                column_id = "col-main"
            elif component_type in ['widget', 'text']:
                column_id = "col-secondary"
            else:
                column_id = "col-sidebar"
            
            # Find the column and add component to it
            column = next((col for col in columns if col.column_id == column_id), columns[0])
            column.component_ids.append(component_id)
            
            # Create component with list position
            component = ListComponentLayout(
                component_id=component_id,
                component_type=component_type,
                position=ListPosition(
                    column_id=column_id,
                    index=len(column.component_ids) - 1,
                    column_width=column.width
                ),
                content=str(element),
                height=self._get_component_height(component_type),
                is_locked=False
            )
            
            components.append(component)
                
        return components, columns

    def _determine_component_type(self, element) -> str:
        """Determine the type of component based on HTML element."""
        tag_name = element.name.lower()
        classes = element.get('class', [])
        
        if tag_name == 'canvas' or any('chart' in c.lower() for c in classes):
            return 'chart'
        elif tag_name == 'table' or any('table' in c.lower() for c in classes):
            return 'table'
        elif any('form' in c.lower() for c in classes):
            return 'form'
        elif any('text' in c.lower() for c in classes):
            return 'text'
        else:
            return 'widget'

    def _get_component_height(self, component_type: str) -> int:
        """Get default height for component type."""
        height_map = {
            'chart': 350,
            'table': 280,
            'form': 400,
            'text': 150,
            'widget': 200
        }
        return height_map.get(component_type, 250)

    def generate_list_layout_html(self, components: List[ListComponentLayout], 
                                columns: List[ListColumn]) -> str:
        """Generate HTML with list/column layout for drag-and-drop."""
        
        # Generate CSS for list layout
        list_css = """
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: white;
            padding: 20px;
        }
        
        .list-container {
            display: flex;
            gap: 20px;
            min-height: 100vh;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .column {
            flex: 1;
            background: #1e293b;
            border-radius: 12px;
            padding: 20px;
            min-height: 600px;
            border: 2px solid #334155;
            transition: all 0.3s ease;
        }
        
        .column.drag-over {
            border-color: #3b82f6;
            background: #1e40af20;
        }
        
        .column-header {
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #334155;
        }
        
        .column-title {
            font-size: 18px;
            font-weight: 600;
            color: #e2e8f0;
            margin-bottom: 5px;
        }
        
        .column-count {
            font-size: 14px;
            color: #94a3b8;
        }
        
        .component-list {
            display: flex;
            flex-direction: column;
            gap: 15px;
            min-height: 400px;
        }
        
        .list-component {
            background: #2d3748;
            border: 2px solid #4a5568;
            border-radius: 8px;
            padding: 15px;
            cursor: move;
            transition: all 0.2s ease;
            user-select: none;
        }
        
        .list-component:hover {
            border-color: #3b82f6;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        
        .list-component.dragging {
            opacity: 0.5;
            transform: rotate(5deg);
            z-index: 1000;
        }
        
        .list-component.locked {
            cursor: not-allowed;
            opacity: 0.6;
            border-color: #6b7280;
        }
        
        .list-component.chart {
            border-left: 4px solid #3b82f6;
        }
        
        .list-component.table {
            border-left: 4px solid #10b981;
        }
        
        .list-component.form {
            border-left: 4px solid #8b5cf6;
        }
        
        .list-component.widget {
            border-left: 4px solid #f59e0b;
        }
        
        .list-component.text {
            border-left: 4px solid #ef4444;
        }
        
        .component-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .component-title {
            font-size: 16px;
            font-weight: 600;
            color: #f1f5f9;
            text-transform: capitalize;
        }
        
        .component-type {
            font-size: 12px;
            color: #94a3b8;
            background: #374151;
            padding: 2px 6px;
            border-radius: 4px;
            margin-left: auto;
        }
        
        .component-content {
            font-size: 14px;
            color: #cbd5e1;
            line-height: 1.4;
        }
        
        .component-id {
            font-size: 11px;
            color: #64748b;
            margin-top: 8px;
            font-family: monospace;
        }
        
        .drop-indicator {
            height: 2px;
            background: #3b82f6;
            margin: 5px 0;
            border-radius: 1px;
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        
        .drop-indicator.active {
            opacity: 1;
        }
        
        .toolbar {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #374151;
            padding: 12px 20px;
            border-radius: 8px;
            display: flex;
            gap: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            z-index: 1001;
        }
        
        .toolbar button {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: background 0.2s ease;
        }
        
        .toolbar button:hover {
            background: #2563eb;
        }
        
        .toolbar button.success {
            background: #10b981;
        }
        
        .toolbar button.success:hover {
            background: #059669;
        }
        
        .empty-column {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 200px;
            border: 2px dashed #4a5568;
            border-radius: 8px;
            color: #6b7280;
            font-style: italic;
        }
        
        .empty-column.drag-over {
            border-color: #3b82f6;
            color: #3b82f6;
        }
        """
        
        # Generate HTML structure
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>List Layout Editor</title>
            <style>
                {list_css}
            </style>
        </head>
        <body>
            <div class="list-container">
        """
        
        # Generate columns
        for column in columns:
            # Get components for this column
            column_components = [comp for comp in components if comp.position.column_id == column.column_id]
            column_components.sort(key=lambda x: x.position.index)
            
            html_content += f"""
                <div class="column" 
                     data-column-id="{column.column_id}"
                     ondragover="onDragOver(event)"
                     ondrop="onDrop(event)"
                     ondragenter="onDragEnter(event)"
                     ondragleave="onDragLeave(event)">
                    
                    <div class="column-header">
                        <div class="column-title">{column.title}</div>
                        <div class="column-count">{len(column_components)} components</div>
                    </div>
                    
                    <div class="component-list" data-column-id="{column.column_id}">
            """
            
            if column_components:
                for component in column_components:
                    component_class = f"list-component {component.component_type}"
                    if component.is_locked:
                        component_class += " locked"
                    
                    html_content += f"""
                        <div class="{component_class}"
                             id="{component.component_id}"
                             data-component-type="{component.component_type}"
                             data-column-id="{column.column_id}"
                             style="min-height: {component.height}px;"
                             draggable="true"
                             ondragstart="onDragStart(event)"
                             ondragend="onDragEnd(event)">
                            
                            <div class="component-header">
                                <div class="component-title">{component.component_type}</div>
                                <div class="component-type">{component.component_type.upper()}</div>
                            </div>
                            
                            <div class="component-content">
                                {component.content}
                            </div>
                            
                            <div class="component-id">{component.component_id}</div>
                        </div>
                    """
            else:
                html_content += f"""
                    <div class="empty-column">
                        Drop components here
                    </div>
                """
            
            html_content += """
                    </div>
                </div>
            """
        
        html_content += """
            </div>
            
            <div class="toolbar">
                <button onclick="saveLayout()">Save Layout</button>
                <button onclick="previewLayout()">Preview</button>
                <button onclick="resetLayout()">Reset</button>
                <button onclick="generateFinal()" class="success">Generate Final Dashboard</button>
            </div>
            
            <script>
                let draggedElement = null;
                let draggedFromColumn = null;
                
                function onDragStart(event) {
                    if (event.target.classList.contains('locked')) {
                        event.preventDefault();
                        return;
                    }
                    
                    draggedElement = event.target;
                    draggedFromColumn = event.target.dataset.columnId;
                    event.target.classList.add('dragging');
                    event.dataTransfer.setData('text/plain', event.target.id);
                    event.dataTransfer.effectAllowed = 'move';
                }
                
                function onDragEnd(event) {
                    if (event.target.classList.contains('locked')) return;
                    
                    event.target.classList.remove('dragging');
                    draggedElement = null;
                    draggedFromColumn = null;
                    
                    // Remove drag over effects
                    document.querySelectorAll('.column').forEach(col => {
                        col.classList.remove('drag-over');
                    });
                }
                
                function onDragEnter(event) {
                    event.preventDefault();
                    event.target.closest('.column').classList.add('drag-over');
                }
                
                function onDragLeave(event) {
                    event.preventDefault();
                    if (!event.target.closest('.column').contains(event.relatedTarget)) {
                        event.target.closest('.column').classList.remove('drag-over');
                    }
                }
                
                function onDragOver(event) {
                    event.preventDefault();
                    event.dataTransfer.dropEffect = 'move';
                }
                
                function onDrop(event) {
                    event.preventDefault();
                    
                    const column = event.target.closest('.column');
                    const componentList = column.querySelector('.component-list');
                    const componentId = event.dataTransfer.getData('text/plain');
                    const component = document.getElementById(componentId);
                    
                    if (!component || component.classList.contains('locked')) return;
                    
                    column.classList.remove('drag-over');
                    
                    // Remove empty column placeholder if it exists
                    const emptyColumn = componentList.querySelector('.empty-column');
                    if (emptyColumn) {
                        emptyColumn.remove();
                    }
                    
                    // Find the position to insert the component
                    const afterElement = getDragAfterElement(componentList, event.clientY);
                    
                    if (afterElement == null) {
                        componentList.appendChild(component);
                    } else {
                        componentList.insertBefore(component, afterElement);
                    }
                    
                    // Update component's column data
                    component.dataset.columnId = column.dataset.columnId;
                    
                    // Add empty column placeholder if the original column is now empty
                    const originalColumn = document.querySelector(`[data-column-id="${draggedFromColumn}"] .component-list`);
                    if (originalColumn && originalColumn.children.length === 0) {
                        originalColumn.innerHTML = '<div class="empty-column">Drop components here</div>';
                    }
                    
                    // Update column counts
                    updateColumnCounts();
                    
                    // Save changes
                    saveLayoutChanges();
                }
                
                function getDragAfterElement(container, y) {
                    const draggableElements = [...container.querySelectorAll('.list-component:not(.dragging)')];
                    
                    return draggableElements.reduce((closest, child) => {
                        const box = child.getBoundingClientRect();
                        const offset = y - box.top - box.height / 2;
                        
                        if (offset < 0 && offset > closest.offset) {
                            return { offset: offset, element: child };
                        } else {
                            return closest;
                        }
                    }, { offset: Number.NEGATIVE_INFINITY }).element;
                }
                
                function updateColumnCounts() {
                    document.querySelectorAll('.column').forEach(column => {
                        const componentCount = column.querySelectorAll('.list-component').length;
                        const countElement = column.querySelector('.column-count');
                        countElement.textContent = `${componentCount} components`;
                    });
                }
                
                function saveLayoutChanges() {
                    const components = [];
                    const columns = [];
                    
                    document.querySelectorAll('.column').forEach(column => {
                        const columnId = column.dataset.columnId;
                        const title = column.querySelector('.column-title').textContent;
                        const componentElements = column.querySelectorAll('.list-component');
                        const componentIds = Array.from(componentElements).map(el => el.id);
                        
                        columns.push({
                            column_id: columnId,
                            title: title,
                            width: 4,
                            component_ids: componentIds
                        });
                        
                        componentElements.forEach((element, index) => {
                            components.push({
                                component_id: element.id,
                                component_type: element.dataset.componentType,
                                position: {
                                    column_id: columnId,
                                    index: index,
                                    column_width: 4
                                },
                                content: element.innerHTML,
                                height: parseInt(element.style.minHeight) || 300,
                                is_locked: element.classList.contains('locked')
                            });
                        });
                    });
                    
                    // Send to backend
                    fetch('/api/dashboard/update-list-dragdrop-layout', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            layout_id: window.layoutId,
                            updated_components: components,
                            updated_columns: columns
                        })
                    });
                }
                
                function saveLayout() {
                    saveLayoutChanges();
                    alert('Layout saved successfully!');
                }
                
                function previewLayout() {
                    // This would open a preview window
                    alert('Preview functionality would open layout preview');
                }
                
                function resetLayout() {
                    if (confirm('Are you sure you want to reset the layout?')) {
                        location.reload();
                    }
                }
                
                function generateFinal() {
                    if (confirm('Generate the final dashboard with current layout?')) {
                        saveLayoutChanges();
                        setTimeout(() => {
                            alert('Final dashboard generation started!');
                        }, 500);
                    }
                }
                
                // Initialize
                updateColumnCounts();
            </script>
        </body>
        </html>
        """
        
        return html_content

    async def update_list_dragdrop_layout(self, request: ListDragDropRequestSchema) -> ListDragDropResponseSchema:
        """Update the list-based drag-and-drop layout with new component positions."""
        
        try:
            # Generate new HTML with updated positions
            updated_html = self.generate_list_layout_html(
                request.updated_components,
                request.updated_columns
            )
            
            # Create updated layout object
            files_obj = {
                "page_title": "List Layout Editor",
                "html": updated_html,
                "css": "",
                "js": ""
            }
            
            # Upload to R2 storage
            hosted_url = await self.r2.upload_to_storage(files_obj, is_final=False)
            
            return ListDragDropResponseSchema(
                layout_id=request.layout_id,
                preview_url=hosted_url,
                success=True,
                columns=request.updated_columns
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"List DragDrop service -> Failed to update layout: {e}"
            )

    async def create_list_dragdrop_layout(self, layout: Layout) -> ListDragDropResponseSchema:
        """Create a list-based drag-and-drop layout from an existing layout."""
        
        try:
            # Extract components from the layout
            components, columns = self.extract_components_from_layout(layout)
            
            # Generate list layout HTML
            list_html = self.generate_list_layout_html(components, columns)
            
            # Create layout object
            files_obj = {
                "page_title": f"List Layout Editor - {layout.page_title}",
                "html": list_html,
                "css": "",
                "js": f"window.layoutId = '{layout.layout_id}';"
            }
            
            # Upload to R2 storage
            hosted_url = await self.r2.upload_to_storage(files_obj, is_final=False)
            
            return ListDragDropResponseSchema(
                layout_id=layout.layout_id,
                preview_url=hosted_url,
                success=True,
                columns=columns
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"List DragDrop service -> Failed to create list layout: {e}"
            )