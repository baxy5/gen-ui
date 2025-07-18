import json
import os
from typing import Annotated
from fastapi import Depends, HTTPException
from agents.dashboard_agent import get_dashboard_agent
from core.store_to_r2 import R2ObjectStorage
from schemas.dashboard_schema import (
    AgentState,
    FinalRequestSchema,
    FinalResponseSchema,
    Layout,
)
from langchain_core.runnables.config import RunnableConfig


class DashboardFinalService:
    """Service for interacting with Dashboard Agent for final dashboard."""

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
            raise RuntimeError(f"Final service -> Failed to load or parse data: {e}")
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                current_dir, "..", "..", "public-mock-data", "component_library.json"
            )
            with open(file_path, "r") as f:
                self.ui_descriptor = json.dumps(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(
                f"Final service -> Failed to load or parse component_library.json: {e}"
            )
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                current_dir, "..", "..", "public-mock-data", "styles.css"
            )
            with open(file_path, "r") as f:
                self.css_descriptor = f.read()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(
                f"Final service -> Failed to load or parse styles.css: {e}"
            )

    async def generate_final(self, request: FinalRequestSchema) -> FinalResponseSchema:
        config = RunnableConfig(configurable={"thread_id": "1"})

        # Get previous state
        selected_layout: Layout = None
        try:
            snapshot = self.agent.graph.get_state(config)
            layouts = snapshot.values["layouts"]

            for layout in layouts:
                if layout.layout_id == request.layout_id:
                    selected_layout = layout
                    break
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Final service -> failed to retrieve conv. history: {e}",
            )

        initial_state: AgentState = {
            "phase": request.phase,
            "selected_layout": selected_layout,
            "ui_descriptor": self.ui_descriptor,
            "design_system": self.css_descriptor,
        }

        result = await self.agent.graph.ainvoke(initial_state, config=config)
        final_result: Layout = result["final"]

        response: FinalResponseSchema = None
        try:
            files_obj = {
                "page_title": final_result.page_title,
                "html": final_result.html,
                "css": final_result.css,
                "js": final_result.js,
            }

            hosted_url = await self.r2.upload_to_storage(files_obj, is_final=True)
            response = FinalResponseSchema(url=hosted_url)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Final service -> Failed to upload to R2 object storage: {e}",
            )

        try:
            if response:
                return response
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Final service -> Failed to return response: {e}",
            )
