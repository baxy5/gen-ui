"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";

interface ListPosition {
  column_id: string;
  index: number;
  column_width: number;
}

interface ListComponentLayout {
  component_id: string;
  component_type: string;
  position: ListPosition;
  content: string;
  height: number;
  is_locked: boolean;
}

interface ListColumn {
  column_id: string;
  title: string;
  width: number;
  component_ids: string[];
}

interface ListDragDropState {
  layout_id: string;
  components: ListComponentLayout[];
  columns: ListColumn[];
  draggedComponent: ListComponentLayout | null;
  draggedFromColumn: string | null;
}

export default function ListLayoutEditor() {
  const searchParams = useSearchParams();
  const layoutId = searchParams.get("layoutId") || "list-default";
  
  const [dragDropState, setDragDropState] = useState<ListDragDropState>({
    layout_id: layoutId,
    components: [],
    columns: [],
    draggedComponent: null,
    draggedFromColumn: null
  });
  
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [dragOverColumn, setDragOverColumn] = useState<string | null>(null);

  // Initialize the list drag-and-drop layout
  useEffect(() => {
    const initializeListDragDropLayout = async () => {
      try {
        setIsLoading(true);
        const response = await fetch(`/api/dashboard/create-list-dragdrop-layout?layout_id=${layoutId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        
        if (!response.ok) {
          throw new Error('Failed to create list drag-drop layout');
        }
        
        const data = await response.json();
        setPreviewUrl(data.preview_url);
        
        // Initialize with sample components and columns
        const sampleColumns: ListColumn[] = [
          {
            column_id: "col-main",
            title: "Main Components",
            width: 4,
            component_ids: ["chart-1", "table-1", "chart-2"]
          },
          {
            column_id: "col-secondary",
            title: "Secondary Components",
            width: 4,
            component_ids: ["widget-1", "widget-2", "text-1"]
          },
          {
            column_id: "col-sidebar",
            title: "Sidebar Components",
            width: 4,
            component_ids: ["form-1", "table-2"]
          }
        ];
        
        const sampleComponents: ListComponentLayout[] = [
          // Main column components
          {
            component_id: "chart-1",
            component_type: "chart",
            position: { column_id: "col-main", index: 0, column_width: 4 },
            content: "<h3>Sales Overview Chart</h3><p>Interactive chart showing sales data over time</p>",
            height: 350,
            is_locked: false
          },
          {
            component_id: "table-1",
            component_type: "table",
            position: { column_id: "col-main", index: 1, column_width: 4 },
            content: "<h3>Customer Data Table</h3><p>Sortable table with customer information</p>",
            height: 280,
            is_locked: false
          },
          {
            component_id: "chart-2",
            component_type: "chart",
            position: { column_id: "col-main", index: 2, column_width: 4 },
            content: "<h3>Revenue Breakdown</h3><p>Pie chart showing revenue by category</p>",
            height: 350,
            is_locked: false
          },
          // Secondary column components
          {
            component_id: "widget-1",
            component_type: "widget",
            position: { column_id: "col-secondary", index: 0, column_width: 4 },
            content: "<h3>KPI Widget</h3><p>Key performance indicators widget</p>",
            height: 200,
            is_locked: false
          },
          {
            component_id: "widget-2",
            component_type: "widget",
            position: { column_id: "col-secondary", index: 1, column_width: 4 },
            content: "<h3>Status Monitor</h3><p>System status monitoring widget</p>",
            height: 200,
            is_locked: false
          },
          {
            component_id: "text-1",
            component_type: "text",
            position: { column_id: "col-secondary", index: 2, column_width: 4 },
            content: "<h3>Information Panel</h3><p>Text-based information display</p>",
            height: 150,
            is_locked: false
          },
          // Sidebar column components
          {
            component_id: "form-1",
            component_type: "form",
            position: { column_id: "col-sidebar", index: 0, column_width: 4 },
            content: "<h3>User Input Form</h3><p>Form for collecting user data</p>",
            height: 400,
            is_locked: false
          },
          {
            component_id: "table-2",
            component_type: "table",
            position: { column_id: "col-sidebar", index: 1, column_width: 4 },
            content: "<h3>Analytics Table</h3><p>Detailed analytics data table</p>",
            height: 280,
            is_locked: false
          }
        ];
        
        setDragDropState(prev => ({
          ...prev,
          components: sampleComponents,
          columns: sampleColumns
        }));
        
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setIsLoading(false);
      }
    };

    initializeListDragDropLayout();
  }, [layoutId]);

  // Handle drag start
  const handleDragStart = (e: React.DragEvent<HTMLDivElement>, component: ListComponentLayout) => {
    if (component.is_locked) {
      e.preventDefault();
      return;
    }
    
    e.dataTransfer.setData("text/plain", component.component_id);
    setDragDropState(prev => ({
      ...prev,
      draggedComponent: component,
      draggedFromColumn: component.position.column_id
    }));
  };

  // Handle drag end
  const handleDragEnd = () => {
    setDragDropState(prev => ({
      ...prev,
      draggedComponent: null,
      draggedFromColumn: null
    }));
    setDragOverColumn(null);
  };

  // Handle drag over column
  const handleDragOver = (e: React.DragEvent<HTMLDivElement>, columnId: string) => {
    e.preventDefault();
    setDragOverColumn(columnId);
  };

  // Handle drag leave column
  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>, columnId: string) => {
    if (!e.currentTarget.contains(e.relatedTarget as Node)) {
      setDragOverColumn(null);
    }
  };

  // Handle drop
  const handleDrop = (e: React.DragEvent<HTMLDivElement>, targetColumnId: string, targetIndex?: number) => {
    e.preventDefault();
    setDragOverColumn(null);
    
    const componentId = e.dataTransfer.getData("text/plain");
    const component = dragDropState.components.find(c => c.component_id === componentId);
    
    if (!component || component.is_locked) return;
    
    const targetColumn = dragDropState.columns.find(c => c.column_id === targetColumnId);
    if (!targetColumn) return;
    
    // Calculate new index if not provided
    const newIndex = targetIndex !== undefined ? targetIndex : targetColumn.component_ids.length;
    
    // Update columns
    const updatedColumns = dragDropState.columns.map(col => {
      if (col.column_id === component.position.column_id) {
        // Remove from source column
        return {
          ...col,
          component_ids: col.component_ids.filter(id => id !== componentId)
        };
      } else if (col.column_id === targetColumnId) {
        // Add to target column
        const newComponentIds = [...col.component_ids];
        newComponentIds.splice(newIndex, 0, componentId);
        return {
          ...col,
          component_ids: newComponentIds
        };
      }
      return col;
    });
    
    // Update components
    const updatedComponents = dragDropState.components.map(comp => {
      if (comp.component_id === componentId) {
        return {
          ...comp,
          position: {
            ...comp.position,
            column_id: targetColumnId,
            index: newIndex
          }
        };
      }
      return comp;
    });
    
    setDragDropState(prev => ({
      ...prev,
      components: updatedComponents,
      columns: updatedColumns
    }));
    
    // Save changes
    saveLayoutChanges(updatedComponents, updatedColumns);
  };

  // Save layout changes
  const saveLayoutChanges = async (components?: ListComponentLayout[], columns?: ListColumn[]) => {
    try {
      const componentsToSave = components || dragDropState.components;
      const columnsToSave = columns || dragDropState.columns;
      
      const response = await fetch('/api/dashboard/update-list-dragdrop-layout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          layout_id: layoutId,
          updated_components: componentsToSave,
          updated_columns: columnsToSave
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to save layout changes');
      }
      
      const data = await response.json();
      setPreviewUrl(data.preview_url);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save changes');
    }
  };

  // Get components for a specific column
  const getComponentsForColumn = (columnId: string): ListComponentLayout[] => {
    return dragDropState.components
      .filter(comp => comp.position.column_id === columnId)
      .sort((a, b) => a.position.index - b.position.index);
  };

  // Get component color by type
  const getComponentColor = (type: string): string => {
    switch (type) {
      case 'chart': return 'border-l-blue-500 bg-blue-50';
      case 'table': return 'border-l-green-500 bg-green-50';
      case 'form': return 'border-l-purple-500 bg-purple-50';
      case 'widget': return 'border-l-yellow-500 bg-yellow-50';
      case 'text': return 'border-l-red-500 bg-red-50';
      default: return 'border-l-gray-500 bg-gray-50';
    }
  };

  // Proceed to final generation
  const proceedToFinal = async () => {
    try {
      const response = await fetch('/api/dashboard/generate-final', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          layout_id: layoutId,
          list_layout: {
            layout_id: layoutId,
            components: dragDropState.components,
            columns: dragDropState.columns,
            layout_style: "kanban"
          }
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate final dashboard');
      }
      
      const data = await response.json();
      window.open(data.url, '_blank');
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate final dashboard');
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="text-white">Loading list layout editor...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="text-red-500">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-6">List Layout Editor</h1>
        
        {/* Controls */}
        <div className="bg-gray-800 rounded-lg p-4 mb-6 flex justify-between items-center">
          <div className="text-white">
            <span className="text-sm text-gray-400">Layout ID: </span>
            <span className="font-mono">{layoutId}</span>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => saveLayoutChanges()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
            >
              Save Layout
            </button>
            <button
              onClick={() => window.open(previewUrl, '_blank')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
              disabled={!previewUrl}
            >
              Preview
            </button>
            <button
              onClick={proceedToFinal}
              className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            >
              Generate Final Dashboard
            </button>
          </div>
        </div>

        {/* List Layout */}
        <div className="flex gap-6 min-h-[600px]">
          {dragDropState.columns.map((column) => {
            const columnComponents = getComponentsForColumn(column.column_id);
            const isDragOver = dragOverColumn === column.column_id;
            
            return (
              <div
                key={column.column_id}
                className={`flex-1 bg-gray-800 rounded-lg p-4 transition-all duration-300 ${
                  isDragOver ? 'bg-blue-900 border-2 border-blue-500' : 'border-2 border-gray-600'
                }`}
                onDragOver={(e) => handleDragOver(e, column.column_id)}
                onDragLeave={(e) => handleDragLeave(e, column.column_id)}
                onDrop={(e) => handleDrop(e, column.column_id)}
              >
                {/* Column Header */}
                <div className="mb-4 pb-4 border-b border-gray-600">
                  <h3 className="text-lg font-semibold text-white">{column.title}</h3>
                  <p className="text-sm text-gray-400">{columnComponents.length} components</p>
                </div>
                
                {/* Component List */}
                <div className="space-y-4">
                  {columnComponents.length === 0 ? (
                    <div className="text-center py-8 text-gray-500 border-2 border-dashed border-gray-600 rounded-lg">
                      Drop components here
                    </div>
                  ) : (
                    columnComponents.map((component) => (
                      <div
                        key={component.component_id}
                        className={`border-2 border-gray-600 rounded-lg p-4 cursor-move transition-all duration-200 hover:border-blue-500 hover:shadow-lg ${
                          getComponentColor(component.component_type)
                        } ${
                          component.is_locked ? 'opacity-60 cursor-not-allowed' : ''
                        } ${
                          dragDropState.draggedComponent?.component_id === component.component_id 
                            ? 'opacity-50 transform rotate-2' 
                            : ''
                        }`}
                        style={{ minHeight: `${component.height}px` }}
                        draggable={!component.is_locked}
                        onDragStart={(e) => handleDragStart(e, component)}
                        onDragEnd={handleDragEnd}
                      >
                        <div className="flex justify-between items-start mb-2">
                          <div className="text-lg font-semibold text-gray-800 capitalize">
                            {component.component_type}
                          </div>
                          <div className="text-xs bg-gray-700 text-white px-2 py-1 rounded">
                            {component.component_type.toUpperCase()}
                          </div>
                        </div>
                        
                        <div 
                          className="text-sm text-gray-700 mb-3"
                          dangerouslySetInnerHTML={{ __html: component.content }}
                        />
                        
                        <div className="text-xs text-gray-500 font-mono">
                          {component.component_id}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
        
        {/* Instructions */}
        <div className="mt-6 bg-gray-800 rounded-lg p-4">
          <h3 className="text-lg font-semibold text-white mb-2">Instructions</h3>
          <ul className="text-gray-300 space-y-1">
            <li>• Drag components between columns to reorganize your layout</li>
            <li>• Components are automatically sorted within each column</li>
            <li>• Each column represents a different area of your dashboard</li>
            <li>• Use "Save Layout" to persist your changes</li>
            <li>• Click "Preview" to see the current layout</li>
            <li>• Click "Generate Final Dashboard" when you're satisfied with the organization</li>
          </ul>
        </div>
      </div>
    </div>
  );
}