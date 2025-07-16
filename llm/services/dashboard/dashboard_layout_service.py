import json
import os
from typing import Annotated, List
from fastapi import Depends, HTTPException
from agents.dashboard_agent import get_dashboard_agent
from core.store_to_r2 import R2ObjectStorage
from schemas.dashboard_schema import (
    AgentState,
    Layout,
    LayoutRequestSchema,
    LayoutResponseSchema,
    LayoutsResponse,
)
from langchain_core.runnables.config import RunnableConfig


class DashboardLayoutService:
    """Service for interacting with Dashboard Agent for three layouts."""

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
        self.agent = get_dashboard_agent()
        self.r2 = r2
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                current_dir, "..", "..", "mock-data", "response_1748851964185.json"
            )
            with open(file_path, "r") as f:
                self.data = json.dumps(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Layout service -> Failed to load or parse data: {e}")
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                current_dir, "..", "..", "public-mock-data", "styles-wire.css"
            )
            with open(file_path, "r") as f:
                self.css_descriptor = f.read()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(
                f"Final service -> Failed to load or parse styles.css: {e}"
            )

    async def generate_layouts(
        self, request: LayoutRequestSchema
    ) -> LayoutResponseSchema:
        config = RunnableConfig(configurable={"thread_id": "1"})

        initial_state: AgentState = {
            "query": request.query,
            "data": self.data,
            "design_system": self.css_descriptor,
            "phase": request.phase,  # "layout"
        }

        result = await self.agent.graph.ainvoke(initial_state, config=config)
        response_layouts: List[Layout] = result["layouts"]

        layouts_response_list: List[LayoutsResponse] = []
        try:
            for layout in response_layouts:
                files_obj = {
                    "page_title": layout.page_title,
                    "html": layout.html,
                    "css": layout.css,
                    "js": layout.js,
                }
                hosted_url = await self.r2.upload_to_storage(files_obj, is_final=False)
                layout_response = LayoutsResponse(
                    url=hosted_url, layout_id=layout.layout_id
                )
                layouts_response_list.append(layout_response)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Layout service -> Failed to upload to R2 object storage: {e}",
            )

        try:
            if layouts_response_list:
                return LayoutResponseSchema(layouts=layouts_response_list)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Layout service -> Failed to return response: {e}",
            )
