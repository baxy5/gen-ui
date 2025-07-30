from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from core.common import get_gpt_client
from schemas.dashboard_schema import AgentState, Layout
from prompts.dashboard_agent_prompts import (
    generate_js_prompt,
    generate_html_with_data_prompt,
    adding_design_system_to_html_prompt,
    generate_js_utils_prompt,
)
from core.logger import get_logger
import os
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()
logger = get_logger("dashboard_agent")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Configure LangSmith
if LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "dashboard-agent"
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")


class DashboardAgent:
    """Agent for generating dashboard."""

    def __init__(self) -> None:
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    @traceable
    def _build_graph(self):
        graph = StateGraph(AgentState)

        #gpt-4.1-mini
        #gpt-4.1
        @traceable
        async def generate_js(state: AgentState):
            client = ChatOpenAI(model="o4-mini", api_key=OPENAI_API_KEY)

            try:
                logger.info("Generating Javascript data schema...")
                messages = [
                    SystemMessage(generate_js_prompt),
                    HumanMessage(
                        f"""
                    User Query: 
                    {state["query"]}
                    
                    Dataset: 
                    {state["data"]}
                """
                    ),
                ]

                response = await client.ainvoke(messages)
                state["js"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during Javascript generation from data: {e}")
                raise Exception(f"Error in generate_js: {e}")

        @traceable
        async def generate_html_with_data(state: AgentState):
            client = ChatOpenAI(model="o4-mini", api_key=OPENAI_API_KEY)

            try:
                logger.info("Generating HTML structure with data...")
                messages = [
                    SystemMessage(generate_html_with_data_prompt),
                    HumanMessage(
                        f"""
                    Javascript constants and arrays which represents the data:
                    {state["js"]}
                    """
                    ),
                ]

                response = await client.ainvoke(messages)
                state["html"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during HTML structure generation: {e}")
                raise Exception(f"Error in generate_html: {e}")

        @traceable
        async def generate_js_utils(state: AgentState):
            client = ChatOpenAI(model="gpt-4.1", api_key=OPENAI_API_KEY)

            class Schema(BaseModel):
                html: str
                js_utils: str

            structured_client = client.with_structured_output(Schema)

            try:
                logger.info("Generating javascript utils...")
                messages = [
                    SystemMessage(generate_js_utils_prompt),
                    HumanMessage(
                        f"""
                        Generated HTML code:
                        {state["html"]}
                        
                        Generated Javascript code:
                        {state["js"]}
                        """
                    ),
                ]

                response = await structured_client.ainvoke(messages)
                state["html"] = response.html
                state["js_utils"] = response.js_utils
                return state

            except Exception as e:
                logger.error(f"Error during JS utils generation: {e}")
                raise Exception(f"Error in generate_js_utils: {e}")

        @traceable
        async def adding_design_system_to_html(state: AgentState):
            client = ChatOpenAI(model="gpt-4.1", api_key=OPENAI_API_KEY)

            try:
                logger.info("Adding desing system classes to html code.")
                messages = [
                    SystemMessage(adding_design_system_to_html_prompt),
                    HumanMessage(
                        f"""
                    Design System (predefined CSS classes):
                    {state["design_system"]}
                    
                    Generated HTML code:
                    {state['html']}
                    
                    Generated Javascript utility functions:
                    {state["js_utils"]}
                    """
                    ),
                ]

                response = await client.ainvoke(messages)
                state["html"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error adding css to html: {e}")
                raise Exception(f"Error in generate_css: {e}")

        graph.add_node("generate_js", generate_js)
        graph.add_node("generate_html_with_data", generate_html_with_data)
        graph.add_node("generate_js_utils", generate_js_utils)
        graph.add_node("adding_design_system_to_html", adding_design_system_to_html)

        graph.set_entry_point("generate_js")
        graph.add_edge("generate_js", "generate_html_with_data")
        graph.add_edge("generate_html_with_data", "generate_js_utils")
        graph.add_edge("generate_js_utils", "adding_design_system_to_html")
        graph.add_edge("adding_design_system_to_html", END)

        return graph.compile(checkpointer=self.checkpoint_saver)
