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

logger = get_logger("dashboard_agent")


class DashboardAgent:
    """Agent for generating dashboard."""

    def __init__(self, client: ChatOpenAI) -> None:
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_js(state: AgentState):
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

                response = await self.client.ainvoke(messages)
                state["js"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during Javascript generation from data: {e}")
                raise Exception(f"Error in generate_js: {e}")

        async def generate_html(state: AgentState):
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

                response = await self.client.ainvoke(messages)
                state["html"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during HTML structure generation: {e}")
                raise Exception(f"Error in generate_html: {e}")

        async def generate_css(state: AgentState):
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

                response = await self.client.ainvoke(messages)
                state["css"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during CSS generation: {e}")
                raise Exception(f"Error in generate_css: {e}")

        async def complete_html_with_css(state: AgentState):
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

                response = await self.client.ainvoke(messages)
                state["html"] = response.content
                return state
            except Exception as e:
                logger.error(f"Error during HTML and CSS combining: {e}")
                raise Exception(f"Error in complete_html_with_css: {e}")

        async def complete_js(state: AgentState):
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

                response = await self.client.ainvoke(messages)
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


# Create a single shared instance
_dashboard_agent_instance = None


def get_dashboard_agent() -> DashboardAgent:
    """Get or create the shared dashboard agent instance."""
    global _dashboard_agent_instance
    if _dashboard_agent_instance is None:
        client = get_gpt_client()
        _dashboard_agent_instance = DashboardAgent(client)
    return _dashboard_agent_instance
