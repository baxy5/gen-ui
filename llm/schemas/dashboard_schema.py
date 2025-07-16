from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field


class LayoutRequestSchema(BaseModel):
    """Schema for API "layout" phase request."""

    query: str = Field(
        default="Create a dashboard from all the provided data.",
        description="User query.",
    )
    data: str = Field(description="Provided dataset by the user.")
    phase: str = Field(
        default="layout",
        description="Phase identifier for the nodes of the Agent. Either 'layout' or 'final'",
    )


class ListPosition(BaseModel):
    """Schema for position in list-based drag-and-drop editor."""
    column_id: str = Field(description="ID of the column/list containing the component")
    index: int = Field(description="Position index within the column (0-based)")
    column_width: int = Field(default=4, description="Width of the column (1-12 scale)")


class ListComponentLayout(BaseModel):
    """Schema for component layout in list-based drag-and-drop editor."""
    component_id: str = Field(description="Unique identifier for the component")
    component_type: str = Field(description="Type of component (chart, table, etc.)")
    position: ListPosition = Field(description="Position of the component in lists")
    content: str = Field(description="HTML content of the component")
    height: int = Field(default=300, description="Height of the component in pixels")
    is_locked: bool = Field(default=False, description="Whether the component is locked from editing")


class ListColumn(BaseModel):
    """Schema for a column in list-based drag-and-drop editor."""
    column_id: str = Field(description="Unique identifier for the column")
    title: str = Field(description="Title of the column")
    width: int = Field(default=4, description="Width of the column (1-12 scale)")
    component_ids: List[str] = Field(default=[], description="Ordered list of component IDs in this column")


class ListDragDropLayoutSchema(BaseModel):
    """Schema for list-based drag-and-drop layout editor."""
    layout_id: str = Field(description="ID of the original layout")
    components: List[ListComponentLayout] = Field(description="List of components with their positions")
    columns: List[ListColumn] = Field(description="List of columns in the layout")
    layout_style: str = Field(default="kanban", description="Layout style (kanban, dashboard, etc.)")


class ListDragDropRequestSchema(BaseModel):
    """Schema for list-based drag-and-drop layout update request."""
    layout_id: str = Field(description="ID of the layout being edited")
    updated_components: List[ListComponentLayout] = Field(description="Updated component positions")
    updated_columns: List[ListColumn] = Field(description="Updated column configurations")
    phase: str = Field(default="list_dragdrop", description="Phase identifier")


class ListDragDropResponseSchema(BaseModel):
    """Schema for list-based drag-and-drop layout response."""
    layout_id: str = Field(description="ID of the layout")
    preview_url: str = Field(description="Preview URL for the updated layout")
    success: bool = Field(description="Whether the update was successful")
    columns: List[ListColumn] = Field(description="Updated column configurations")


class FinalRequestSchema(BaseModel):
    """Schema for API "final" phase request."""

    phase: str = Field(
        default="final",
        description="Phase identifier for the nodes of the Agent. Either 'layout' or 'final'",
    )
    layout_id: str = Field(
        description="Selected layout by the user. Only needed in 'final' node."
    )
    list_layout: Optional[ListDragDropLayoutSchema] = Field(
        default=None,
        description="List-based drag-and-drop layout modifications if any"
    )


class LayoutsResponse(BaseModel):
    """Schema for "layouts" in LayoutResponseSchema."""

    url: str = Field(description="R2 public url for displaying in Iframe.")
    layout_id: str


class LayoutResponseSchema(BaseModel):
    """Schema for API "layout" phase response."""

    layouts: List[LayoutsResponse] = Field(description="Information for each layout.")


class FinalResponseSchema(BaseModel):
    """Schema for API "final" phase response."""

    url: str = Field(description="R2 public url for final dashboard.")


class Layout(BaseModel):
    layout_id: str
    page_title: str
    html: str
    css: str
    js: str


class LayoutNode(BaseModel):
    """Schema for the Layout generation node of the Agent workflow."""

    layouts: List[Layout] = Field(description="Three layouts.")


class FinalNode(BaseModel):
    """Schema for the final generation node of the Agent workflow."""

    layout: Layout


class AgentState(TypedDict):
    """State schema of the Agent workflow."""

    query: str = Field(description="User query.")
    data: str = Field(description="Provided dataset by the user.")
    relevant_data: str = Field(
        description="Chosen relevant data for user query from all the data."
    )
    ui_descriptor: str = Field(description="Descriptors of the UI/DS elements.")
    design_system: str = Field(
        description="CSS classes and descriptors of a design system."
    )
    phase: str = Field(
        description="Phase identifier for the nodes of the Agent. Either 'layout' or 'final'"
    )
    selected_layout: Layout = Field(description="Selected layout by the user.")
    layouts: List[Layout] = Field(description="The three layouts for service.")
    final: Layout = Field(description="Final layout for service.")
