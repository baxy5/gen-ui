from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field


class RequestSchema(BaseModel):
    query: str = Field(
        default="Create a business dashboard from the data.",
        description="User query.",
    )


class ResponseSchema(BaseModel):
    url: str = Field(description="R2 public url for final dashboard.")


class Layout(BaseModel):
    layout_id: str
    page_title: str
    html: str
    css: str
    js: str


class AgentState(TypedDict):
    query: str
    data: str
    js: str
    html: str
    css: str
    design_system: str
    dashboard: Layout
