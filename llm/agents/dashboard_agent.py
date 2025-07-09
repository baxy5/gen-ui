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
                    f"""Apply DATA-DRIVEN INFORMATION ARCHITECTURE to create 3 comprehensive dashboard layouts:

                    **USER REQUEST:** {state['query']}
                    **COMPREHENSIVE DATASET:** {state['data']}

                    **ANALYSIS REQUIREMENTS:**
                    1. Extract and utilize EVERY piece of data provided
                    2. Create information hierarchies based on business impact
                    3. Apply systematic component selection based on data characteristics
                    4. Design layouts that facilitate data-driven decision making
                    5. Use CSS classes from the design system for consistent styling

                    **OUTPUT REQUIREMENTS:**
                    - 3 distinct layout approaches (layout-1, layout-2, layout-3) with different component hierarchies
                    - Comprehensive use of ALL provided data in each layout (same data, different structure)
                    - Clear component hierarchy differentiation in each layout
                    - Proper CSS Grid/Flexbox organization using design system classes
                    - Responsive design with centered alignment
                    - Professional styling using design system classes (cards, buttons, text, spacing, colors)
                    - UI component library patterns for consistent visual design

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
                    f"""Create the final comprehensive dashboard using DATA-DRIVEN INFORMATION ARCHITECTURE:

                    **SELECTED LAYOUT:** {state['selected_layout']}
                    **LAYOUT STRUCTURE DESCRIPTION:** {layout_description}
                    **UI COMPONENT LIBRARY:** {state['ui_descriptor']}
                    **CSS DESIGN SYSTEM:** {state['design_system']}

                    **CRITICAL IMPLEMENTATION REQUIREMENTS:**
                    1. **PRESERVE EXACT STRUCTURE**: Use the selected layout's HTML structure EXACTLY as provided - do NOT modify the structure, component types, or data organization
                    2. **FOLLOW LAYOUT DESCRIPTION**: Use the layout structure description as your guide to maintain the exact row/column organization
                    3. **MAINTAIN SAME DATA**: Keep the SAME data points in the SAME locations as shown in the selected layout
                    4. **USE DESIGN SYSTEM CLASSES**: Apply CSS classes from the CSS design system for ALL styling - buttons, cards, text, spacing, colors, layouts
                    5. **UI COMPONENT LIBRARY**: Use components from the UI descriptor library for consistent styling patterns
                    6. **ONLY ENHANCE**: Add better styling, interactivity, and Chart.js visualizations WITHOUT changing the layout structure
                    7. **FIXED CHART DIMENSIONS**: All Chart.js charts MUST have fixed container dimensions (use width: 400px, height: 250px as default)
                    8. **Chart Container Pattern**: Wrap all charts in divs with explicit width/height and position: relative
                    9. **RESPONSIVE DESIGN**: Maintain responsive behavior while keeping chart containers sized properly
                    10. **NO INLINE STYLES**: Use design system classes instead of inline styles wherever possible

                    **LAYOUT STRUCTURE IMPLEMENTATION:**
                    - **MANDATORY**: Follow the layout description exactly for row/column organization
                    - **MANDATORY**: Maintain the same component types in the same positions
                    - **MANDATORY**: Preserve the visual hierarchy described in the layout description
                    - **MANDATORY**: Keep the same data groupings and relationships as described

                    **CHART.JS SIZING REQUIREMENTS:**
                    - MANDATORY: Wrap each chart in a container div with fixed dimensions
                    - MANDATORY: Use style="position: relative; width: 400px; height: 250px;" on chart containers
                    - MANDATORY: Set maintainAspectRatio: false in Chart.js options
                    - MANDATORY: Set responsive: true for mobile compatibility

                    **FINAL OUTPUT:**
                    - Complete dashboard with title, HTML, CSS, and JavaScript
                    - EXACT same structure and data as the selected layout following the layout description
                    - Enhanced styling using CSS classes from the provided design system
                    - UI components from the component library with consistent styling patterns
                    - Interactive features and properly sized Chart.js visualizations
                    - Professional presentation suitable for executive use
                    - Ready for production deployment in iframe environment

                    **CSS DESIGN SYSTEM USAGE:**
                    - Use design system classes for buttons, cards, text styling, spacing, colors, and layouts
                    - Apply UI component library patterns for consistent visual design
                    - Leverage CSS variables and utility classes from the design system
                    - Maintain design system consistency across all components

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
