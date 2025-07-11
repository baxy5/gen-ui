from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from core.common import get_gpt_client
from schemas.dashboard_schema import AgentState, Layout, LayoutNode
from prompts.dashboard_agent_prompts import (
    generate_layout_system_prompt,
    generate_final_layout_description_prompt,
    generate_final_system_prompt,
)


class DashboardAgent:
    """Agent for generating dashboard layouts using data-driven information architecture."""

    def __init__(self, client: ChatOpenAI) -> None:
        self.client = client
        self.checkpoint_saver = InMemorySaver()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(AgentState)

        async def generate_layouts(state: AgentState):
            """Generate three layouts using data-driven information architecture approach."""
            structured_model = self.client.with_structured_output(LayoutNode)
            messages = [
                SystemMessage(generate_layout_system_prompt),
                HumanMessage(
                    f"""
                    Create three comprehensive dashboard layouts from the provided informations.

                    **USER REQUEST:** {state['query']}
                    **DATASET:** {state['data']}
                    **DESIGN SYSTEM:** {state['design_system']}

                    **OUTPUT REQUIREMENTS:**
                    - 3 distinct layout approaches (layout-1, layout-2, layout-3) with different component hierarchies
                    - Comprehensive use of ALL provided data in each layout (same data, different structure)
                    - Clear component hierarchy differentiation in each layout
                    - Proper CSS Grid/Flexbox organization using design system classes
                    - Responsive design with centered alignment
                    - Professional styling using design system classes (cards, buttons, text, spacing, colors)

                    **IMPORTANT:**
                    - Create 3 layout.

                    Focus on creating layouts that help users understand and analyze the complete dataset, not just highlights. Use design system classes for all styling to ensure consistency."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["layouts"] = response.layouts
            return state

        async def finalize_dashboard(
            state: AgentState,
        ) -> AgentState:
            """Finalize dashboard using data-driven architecture principles."""

            # Detailed layout description
            layout_description_messages = [
                SystemMessage(generate_final_layout_description_prompt),
                HumanMessage(
                    f"""Analyze the selected layout and create a detailed structural description:

                    **SELECTED LAYOUT:** {state['selected_layout']}

                    **ANALYSIS REQUIREMENTS:**
                    1. Break down the layout into rows and columns
                    2. Identify component types and their positions
                    3. Describe the visual hierarchy and flow
                    4. Note any spanning or merged sections
                    5. Capture the responsive organization

                    **OUTPUT:** A clear, implementable structural description that captures the exact layout organization."""
                ),
            ]

            layout_description = await self.client.ainvoke(layout_description_messages)

            structured_model = self.client.with_structured_output(Layout)

            messages = [
                SystemMessage(generate_final_system_prompt),
                HumanMessage(
                    f"""Create the final comprehensive dashboard, component(s) or chart(s):

                    **SELECTED LAYOUT:** {state['selected_layout']}
                    **LAYOUT STRUCTURE DESCRIPTION:** {layout_description}
                    **UI COMPONENT LIBRARY:** {state['ui_descriptor']}
                    **CSS DESIGN SYSTEM:** {state['design_system']}

                    **REMEMBER**: Your job is to take the selected layout and enhance it with better styling and interactivity using the design system classes, NOT to redesign or restructure it. The layout structure must remain identical while applying proper CSS classes. Use the layout description as your structural guide. Use the CSS DESIGN SYSTEM as your styling guide."""
                ),
            ]

            response = await structured_model.ainvoke(messages)

            state["final"] = response
            return state

        def route_phase_node(state: AgentState) -> AgentState:
            # This node just passes through the state
            return state

        def route_phase_condition(state: AgentState) -> str:
            # This function determines which path to take
            if state["phase"] == "layout":
                return "layout"
            else:
                return "final"

        graph.add_node("route_phase", route_phase_node)
        graph.add_node("generate_layouts", generate_layouts)
        graph.add_node("finalize_dashboard", finalize_dashboard)

        graph.set_entry_point("route_phase")
        graph.add_conditional_edges(
            "route_phase",
            route_phase_condition,
            {
                "layout": "generate_layouts",
                "final": "finalize_dashboard",
            },
        )

        graph.add_edge("generate_layouts", END)
        graph.add_edge("finalize_dashboard", END)

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
