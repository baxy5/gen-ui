from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.dashboard.dashboard_final_service import DashboardFinalService
from services.dashboard.dashboard_layout_service import DashboardLayoutService
from services.dashboard.dashboard_list_dragdrop_service import DashboardListDragDropService
from schemas.dashboard_schema import (
    FinalRequestSchema,
    FinalResponseSchema,
    LayoutRequestSchema,
    LayoutResponseSchema,
    ListDragDropRequestSchema,
    ListDragDropResponseSchema,
)


router = APIRouter()


@router.post("/generate-layouts")
async def generate_layouts(
    request: LayoutRequestSchema, service: Annotated[DashboardLayoutService, Depends()]
) -> LayoutResponseSchema:
    request.phase = "layout"

    try:
        return await service.generate_layouts(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Layout api -> Failed to generate dashboard: {e}",
        )


@router.post("/create-list-dragdrop-layout")
async def create_list_dragdrop_layout(
    layout_id: str, 
    service: Annotated[DashboardListDragDropService, Depends()],
    layout_service: Annotated[DashboardLayoutService, Depends()]
) -> ListDragDropResponseSchema:
    """Create a list-based drag-and-drop layout editor from an existing layout."""
    
    try:
        # Create a mock layout for demonstration
        # In a real implementation, you'd retrieve the actual layout
        from schemas.dashboard_schema import Layout
        
        layout = Layout(
            layout_id=layout_id,
            page_title="Sample List Layout",
            html="""
            <div class="dashboard">
                <div class="chart-component" id="chart-1">
                    <h3>Sales Overview Chart</h3>
                    <p>Interactive chart showing sales data over time</p>
                </div>
                <div class="table-component" id="table-1">
                    <h3>Customer Data Table</h3>
                    <p>Sortable table with customer information</p>
                </div>
                <div class="chart-component" id="chart-2">
                    <h3>Revenue Breakdown</h3>
                    <p>Pie chart showing revenue by category</p>
                </div>
                <div class="widget-component" id="widget-1">
                    <h3>KPI Widget</h3>
                    <p>Key performance indicators widget</p>
                </div>
                <div class="widget-component" id="widget-2">
                    <h3>Status Monitor</h3>
                    <p>System status monitoring widget</p>
                </div>
                <div class="form-component" id="form-1">
                    <h3>User Input Form</h3>
                    <p>Form for collecting user data</p>
                </div>
                <div class="text-component" id="text-1">
                    <h3>Information Panel</h3>
                    <p>Text-based information display</p>
                </div>
                <div class="table-component" id="table-2">
                    <h3>Analytics Table</h3>
                    <p>Detailed analytics data table</p>
                </div>
            </div>
            """,
            css="",
            js=""
        )
        
        return await service.create_list_dragdrop_layout(layout)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"List DragDrop api -> Failed to create list drag-drop layout: {e}",
        )


@router.post("/update-list-dragdrop-layout")
async def update_list_dragdrop_layout(
    request: ListDragDropRequestSchema, 
    service: Annotated[DashboardListDragDropService, Depends()]
) -> ListDragDropResponseSchema:
    """Update the list-based drag-and-drop layout with new component positions."""
    
    try:
        return await service.update_list_dragdrop_layout(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"List DragDrop api -> Failed to update list drag-drop layout: {e}",
        )


@router.post("/generate-final")
async def generate_final_dashboard(
    request: FinalRequestSchema, service: Annotated[DashboardFinalService, Depends()]
) -> FinalResponseSchema:
    request.phase = "final"

    try:
        return await service.generate_final(request)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Final api -> Failed to generate dashboard: {e}"
        )
