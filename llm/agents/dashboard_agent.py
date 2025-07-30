from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from core.common import get_gpt_client
from schemas.dashboard_schema import AgentState, Layout
from prompts.dashboard_agent_prompts import (
    generate_js_prompt,
    generate_html_prompt,
    generate_css_prompt,
    complete_html_with_css_prompt,
    complete_js_prompt,
    generate_dashboard_prompt,
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

        @traceable
        async def generate_js(state: AgentState):
            client = ChatOpenAI(model="gpt-4.1", api_key=OPENAI_API_KEY)

            try:
                logger.info("Generating Javascript code from data.")
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
        async def generate_html(state: AgentState):
            client = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)

            try:
                logger.info("Generating HTML structure.")
                messages = [
                    SystemMessage(generate_html_prompt),
                    HumanMessage(
                        f"""
                    Javascript code:
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

        # gpt-4.1
        @traceable
        async def generate_css(state: AgentState):
            client = ChatOpenAI(model="gpt-4.1", api_key=OPENAI_API_KEY)

            try:
                logger.info("Generating CSS code.")
                messages = [
                    SystemMessage(generate_css_prompt),
                    HumanMessage(
                        f"""
                    Design System:
                    {state["design_system"]}
                    
                    HTML:
                    {state['html']}
                    """
                    ),
                ]

                response = await client.ainvoke(messages)
                state["css"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during CSS generation: {e}")
                raise Exception(f"Error in generate_css: {e}")

        @traceable
        async def complete_html_with_css(state: AgentState):
            client = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)

            try:
                logger.info("Generating combined HTML and CSS code.")
                messages = [
                    SystemMessage(complete_html_with_css_prompt),
                    HumanMessage(
                        f"""
                    HTML code:
                    {state['html']}
                    
                    CSS code:
                    {state["css"]}
                    """
                    ),
                ]

                response = await client.ainvoke(messages)
                state["html"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during HTML and CSS combining: {e}")
                raise Exception(f"Error in complete_html_with_css: {e}")

        @traceable
        async def complete_js(state: AgentState):
            client = ChatOpenAI(model="gpt-4.1-mini", api_key=OPENAI_API_KEY)

            try:
                logger.info("Completing the Javascript code.")
                messages = [
                    SystemMessage(complete_js_prompt),
                    HumanMessage(
                        f"""
                    Javascript code:
                    {state["js"]}
                    """
                    ),
                ]

                response = await client.ainvoke(messages)
                state["js"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during Javascript code complatetation: {e}")
                raise Exception(f"Error in complete_js: {e}")

        """ async def generate_dashboard(state: AgentState):
            structured_model = self.client.with_structured_output(Layout)
            messages = [
                SystemMessage(generate_dashboard_prompt),
                HumanMessage(),
            ]

            response = await structured_model.ainvoke(messages)
            state["dashboard"] = response
            return state """

        graph.add_node("generate_js", generate_js)
        graph.add_node("generate_html", generate_html)
        graph.add_node("generate_css", generate_css)
        graph.add_node("complete_html_with_css", complete_html_with_css)
        graph.add_node("complete_js", complete_js)

        graph.set_entry_point("generate_js")
        graph.add_edge("generate_js", "generate_html")
        graph.add_edge("generate_html", "generate_css")
        graph.add_edge("generate_css", "complete_html_with_css")
        graph.add_edge("complete_html_with_css", "complete_js")
        graph.add_edge("complete_js", END)

        return graph.compile(checkpointer=self.checkpoint_saver)
