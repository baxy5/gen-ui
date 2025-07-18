from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from core.common import get_gpt_client
from schemas.dashboard_schema import AgentState, Layout
from prompts.dashboard_agent_prompts import (
    generate_js_prompt,
    generate_dashboard_prompt,
)


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
                raise Exception(f"Error in generate_js: {e}")

        async def generate_html(state: AgentState):
            try:
                messages = [
                    SystemMessage(
                        """
                    You are a senior front-end developer, skilled in building responsive, interactive, and visually polished web applications.
                    
                    Your task:  
                    Generate a **semantic, responsive HTML structure** that is designed to be dynamically populated using a **JavaScript dataset** (provided in the input).

                    Instructions:
                    - Do not hardcode any data values.
                    - Add placeholder elements or `id`/`data-*` attributes where JavaScript can inject the data later.
                    - Use semantic tags like `<main>`, `<section>`, `<article>`, `<table>`, `<thead>`, `<tbody>`, etc.
                    - Structure the layout based on the data format: if it's tabular, use `<table>`; if hierarchical, consider lists or expandable sections.
                    - Add proper classes and clear markup structure so styling and scripting can hook in cleanly.
                    - Ensure accessibility and mobile responsiveness using semantic tags and good nesting.

                    Return only the HTML (do not include CSS or JS).
                    """
                    ),
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
                raise Exception(f"Error in generate_html: {e}")

        async def generate_css(state: AgentState):
            try:
                messages = [
                    SystemMessage(
                        f"""
                    You are a senior front-end developer, skilled in building responsive, interactive, and visually polished web applications.
                    
                    Your task:
                    Generate a CSS code for a modern, responsive web application.
                    
                    Instructions:
                    - Use the predefined classes from the design system.
                    - Do not generate other color variables.
                    - If a necessary CSS class in not in the design system, generate it.
                    """
                    ),
                    HumanMessage(
                        f"""
                    Design System:
                    {state["design_system"]}
                    """
                    ),
                ]

                response = await self.client.ainvoke(messages)
                state["css"] = response.content
                return state
            except Exception as e:
                raise Exception(f"Error in generate_css: {e}")

        async def complete_html_with_css(state: AgentState):
            try:
                messages = [
                    SystemMessage(
                        f"""
                    You are a senior front-end developer, skilled in building responsive, interactive, and visually polished web applications.
                    
                    Your task:
                    Refactor the HTML code to use the CSS classes from the provided CSS code.
                    
                    Instructions:
                    - Do not change the layout structure of the HTML elements.
                    - Only implement the CSS classes on the HTML elements.
                    """
                    ),
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
                raise Exception(f"Error in complete_html_with_css: {e}")

        async def complete_js(state: AgentState):
            try:
                messages = [
                    SystemMessage(
                        f"""
                    You are a senior front-end developer, skilled in building responsive, interactive, and visually polished web applications.
                    
                    Your task:
                    Complete the provided Javascript code which means, extend with utility functions, fill the HTML with the provided data,
                    generate input search functions, filtering functions, modal functionalities.
                    
                    Instructions:
                    - Do not remove the provided Javascript code just extend it.
                    - Add only necessary functions.
                    """
                    ),
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
