from typing import Annotated, List, Optional, TypedDict, Union
from fastapi import Depends
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from core.common import get_gpt_client
from schemas.dashboard_schema import AgentState, Layout, LayoutNode


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
                SystemMessage(
                    """You are a senior data analyst and UI architect specializing in comprehensive dashboard design. 
                    Generate 3 distinct layout approaches for the provided data and user request.

                    ## CORE METHODOLOGY: COMPREHENSIVE DATA ANALYSIS

                    ### STEP 1: COMPLETE DATA INVENTORY
                    - Analyze EVERY piece of data provided - numbers, percentages, categories, time series, hierarchies
                    - Identify data types: KPIs, trends, comparisons, distributions, relationships, historical patterns
                    - Map data relationships and dependencies
                    - Calculate derivative insights (growth rates, ratios, percentages, trends)
                    - Categorize data by business importance and user decision-making impact

                    ### STEP 2: INFORMATION HIERARCHY DESIGN
                    - **PRIMARY LEVEL**: Most critical business metrics that drive decisions (revenue, growth, performance)
                    - **SECONDARY LEVEL**: Supporting metrics that provide context (costs, margins, efficiency)
                    - **TERTIARY LEVEL**: Detailed breakdowns and granular data (departments, subcategories, trends)
                    - **CONTEXTUAL LEVEL**: Comparative and historical data for benchmarking

                    ### STEP 3: SYSTEMATIC COMPONENT SELECTION
                    **For each data element, choose the optimal component based on data characteristics:**
                    
                    **KPI BOXES**: Single critical metrics (revenue, profit, growth %, key ratios)
                    **HERO CARDS**: Important metrics with context (revenue with growth trend, customer count with retention)
                    **COMPARISON CARDS**: Side-by-side metrics (this year vs last year, plan vs actual)
                    **DATA TABLES**: Detailed breakdowns with multiple attributes (product performance, regional data, time series)
                    **CHART CONTAINERS**: Trend data, distributions, comparisons requiring visualization
                    **CHART.JS VISUALIZATIONS**: Interactive charts for complex data (line, bar, pie, doughnut, scatter, radar)
                    **GROUPED SECTIONS**: Related metrics organized by business function or category

                    ### CHART.JS INTEGRATION
                    **Chart.js is available for creating interactive data visualizations:**
                    - **Line Charts**: Time series data, trends, performance over time
                    - **Bar Charts**: Comparisons, categorical data, rankings
                    - **Pie/Doughnut Charts**: Proportions, market share, composition
                    - **Scatter Charts**: Correlations, data relationships
                    - **Radar Charts**: Multi-dimensional data, performance metrics
                    - **Mixed Charts**: Combining multiple chart types for comprehensive analysis
                    - **Canvas-based rendering**: High performance for large datasets
                    - **Responsive and interactive**: Touch/mouse interactions, animations
                    - **Customizable**: Colors, fonts, legends, tooltips, animations

                    ### STEP 4: LAYOUT STRATEGY
                    - **TOP SECTION**: Hero KPIs and primary metrics in a prominent stats grid
                    - **MIDDLE SECTION**: Secondary metrics organized by business function/category
                    - **BOTTOM SECTION**: Detailed data tables and granular breakdowns
                    - **RESPONSIVE GRID**: Use CSS Grid for consistent alignment and responsive behavior
                    - **LOGICAL GROUPING**: Group related information using flexbox containers

                    ### REQUIREMENTS:
                    - **MANDATORY**: Use ALL data provided - create visualizations for every metric
                    - **MANDATORY**: Apply consistent information hierarchy principles
                    - **MANDATORY**: Use proper CSS Grid and Flexbox for layout organization
                    - **MANDATORY**: Create exactly 3 distinct layout approaches with format: layout-[1|2|3]
                    - **MANDATORY**: Provide descriptive page titles that reflect the data content
                    - **MANDATORY**: Hardcode all data values directly into HTML elements
                    - **MANDATORY**: Use CSS classes from the design system for styling (cards, buttons, text, spacing, colors)
                    - **MANDATORY**: Apply UI component library patterns for consistent visual design
                    - **MANDATORY**: Create responsive, center-aligned layouts using design system classes

                    ### LAYOUT DIFFERENTIATION (COMPONENT HIERARCHY FOCUS):
                    **Layout 1**: Grid-Heavy Layout (Card-based layout with KPI grid sections and tabular data breakdowns)
                    **Layout 2**: Chart-Centric Layout (Visualization-focused with charts as primary components, supported by metric cards)
                    **Layout 3**: Mixed Component Layout (Balanced mix of hero cards, data tables, and embedded charts in sections)
                    
                    **IMPORTANT**: All layouts must use the SAME data from the user request - only the component hierarchy, arrangement, and visual structure should differ. Do not filter or change the data content.
                    
                    **Color Accessibility**: Always ensure sufficient contrast ratios (4.5:1 minimum) between text and background colors.
                    **IMPORTANT**: The text color and the background color must be differ.

                    Generate 3 distinct layouts, each showcasing different information architecture approaches while using ALL available data."""
                ),
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
                SystemMessage(
                    """You are a senior UI/UX architect specializing in layout structure analysis. Your task is to analyze the selected layout and create a detailed structural description that captures the exact layout organization.

                    ## LAYOUT ANALYSIS METHODOLOGY:

                    ### 1. STRUCTURAL DECOMPOSITION
                    - **GRID ANALYSIS**: Identify rows, columns, and their arrangements
                    - **COMPONENT POSITIONING**: Map where each component is located
                    - **LAYOUT PATTERNS**: Describe the visual hierarchy and flow
                    - **RESPONSIVENESS**: Note how components are organized for different screen sizes

                    ### 2. DESCRIPTION FORMAT
                    Create a clear, implementable description using this format:
                    - **Row 1**: [Number] columns - [Component types and their purposes]
                    - **Row 2**: [Number] columns - [Component types and their purposes]
                    - **Row 3**: [Merged/Spanning] layout - [Component types and their purposes]
                    - etc.

                    ### 3. COMPONENT IDENTIFICATION
                    - **KPI Cards**: Single metric displays
                    - **Hero Cards**: Featured metrics with context
                    - **Data Tables**: Tabular data displays
                    - **Chart Containers**: Visualization areas
                    - **Stats Grids**: Multiple related metrics
                    - **Section Headers**: Organizational elements

                    ### 4. LAYOUT RELATIONSHIPS
                    - **Column Spans**: How components spread across columns
                    - **Row Heights**: Relative sizing of rows
                    - **Alignment**: How components align within their containers
                    - **Spacing**: Gaps and margins between components

                    ### EXAMPLE OUTPUT:
                    "Row 1: 3 equal columns - KPI card (Revenue), KPI card (Growth), KPI card (Customers)
                    Row 2: 2 columns - Left: Stats grid (4 metrics), Right: Chart container (trend visualization)
                    Row 3: 1 full-width column - Data table (product performance with 6 columns)
                    Row 4: 3 equal columns - Hero card (Sales), Hero card (Marketing), Hero card (Operations)"

                    Provide a clear, structural description that can be used to recreate the exact layout organization."""
                ),
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
                SystemMessage(
                    """You are a senior dashboard architect specializing in DATA-DRIVEN INFORMATION ARCHITECTURE. Your task is to create a comprehensive, professional dashboard that EXACTLY MATCHES the selected layout structure.

                    ## CRITICAL REQUIREMENT: MAINTAIN EXACT LAYOUT STRUCTURE
                    - **MANDATORY**: Use the EXACT same HTML structure as the selected layout
                    - **MANDATORY**: Keep the SAME component types in the SAME positions
                    - **MANDATORY**: Maintain the SAME data groupings and organization
                    - **MANDATORY**: Preserve the SAME visual hierarchy and flow
                    - **MANDATORY**: Do NOT add, remove, or rearrange components from the selected layout
                    - **MANDATORY**: Only enhance styling and add interactivity, never change structure

                    ## FINALIZATION METHODOLOGY:

                    ### 1. EXACT LAYOUT PRESERVATION
                    - Use the selected layout's HTML structure as the foundation - DO NOT MODIFY
                    - Implement EVERY data point EXACTLY as shown in the selected layout
                    - Maintain the same component types, positions, and data groupings
                    - Preserve the exact visual hierarchy and information flow
                    - Only enhance with better styling and interactive features

                    ### 2. ADVANCED STYLING INTEGRATION
                    - **CSS SYSTEM**: MANDATORY use of provided CSS classes and design tokens from the CSS design system
                    - **COMPONENT LIBRARY**: Use appropriate components from the UI descriptor library (cards, stats, forms, status badges)
                    - **LAYOUT SYSTEM**: Implement proper CSS Grid and Flexbox layouts using design system classes
                    - **RESPONSIVE DESIGN**: Ensure components adapt to different screen sizes using design system responsive classes
                    - **VISUAL HIERARCHY**: Use typography, spacing, and color classes from the design system to guide user attention
                    - **DESIGN SYSTEM CLASSES**: Apply CSS classes from the design system for consistent styling (buttons, cards, text, spacing, colors)
                    - **NO INLINE STYLES**: Use design system classes instead of inline styles wherever possible

                    ### 3. INTERACTIVE DASHBOARD FEATURES
                    - **Dynamic Data Binding**: Create JavaScript that makes data interactive
                    - **Chart.js Integration**: Implement interactive charts for data visualization
                    - **Filtering & Sorting**: Add controls for data exploration
                    - **Drill-down Capabilities**: Enable users to explore details
                    - **Real-time Updates**: Implement functions for data refreshing
                    - **Export Functionality**: Add options to export or share data

                    ### CHART.JS IMPLEMENTATION GUIDE
                    **Chart.js is pre-loaded and available for creating interactive visualizations:**
                    - **Canvas Elements**: Use `<canvas>` tags with unique IDs for each chart
                    - **Chart Configuration**: Configure charts with data, options, and styling
                    - **Responsive Charts**: Set `responsive: true` and `maintainAspectRatio: false`
                    - **Color Schemes**: Use consistent color palettes across charts
                    - **Interactive Features**: Enable tooltips, legends, and hover effects
                    - **Data Updates**: Implement functions to update chart data dynamically
                    - **Multiple Chart Types**: Line, bar, pie, doughnut, scatter, radar, and mixed charts
                    - **Performance**: Leverage canvas rendering for smooth performance with large datasets

                    **CRITICAL: Chart Sizing and Container Requirements:**
                    - **MANDATORY**: Set fixed dimensions on chart containers to prevent infinite expansion
                    - **MANDATORY**: Use CSS to set explicit width and height on chart containers
                    - **MANDATORY**: Set `maintainAspectRatio: false` in Chart.js options
                    - **MANDATORY**: Use `responsive: true` for mobile compatibility
                    - **RECOMMENDED**: Standard chart sizes: 400px width, 250px height for most charts
                    - **RECOMMENDED**: Larger charts: 600px width, 350px height for main visualizations

                    **Example Chart Implementation with Fixed Sizing:**
                    ```html
                    <div class="chart-container" style="position: relative; width: 400px; height: 250px;">
                        <canvas id="myChart"></canvas>
                    </div>
                    ```
                    ```javascript
                    const ctx = document.getElementById('myChart').getContext('2d');
                    const myChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                            datasets: [{
                                label: 'Sales',
                                data: [12, 19, 3, 5, 2, 3],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: {
                                    display: true,
                                    position: 'top'
                                }
                            }
                        }
                    });
                    ```

                    ### 4. PROFESSIONAL IMPLEMENTATION
                    - **Semantic HTML**: Use proper HTML5 structure with accessibility
                    - **CSS Architecture**: Build upon provided styles with additional enhancements
                    - **JavaScript Logic**: Create interactive features and data manipulation
                    - **Error Handling**: Implement graceful error states and loading indicators
                    - **Performance**: Optimize for fast rendering and smooth interactions

                    ### 5. PERPLEXITY LABS STYLE
                    - **Modern Design**: Clean, minimal interface with strategic use of white space
                    - **Data-First Approach**: Prioritize data visibility and accessibility
                    - **Professional Typography**: Clear hierarchy and readable fonts
                    - **Subtle Animations**: Smooth transitions and hover effects
                    - **Intelligent Grouping**: Logical organization of related information

                    ### QUALITY STANDARDS:
                    - **Complete Data Coverage**: Every metric from the dataset should be represented
                    - **Professional Styling**: Consistent use of design system and CSS classes
                    - **Interactive Elements**: Functional JavaScript for data exploration
                    - **Responsive Layout**: Works perfectly across all device sizes
                    - **Self-contained**: Ready to deploy in iframe without external dependencies

                    ### OUTPUT REQUIREMENTS:
                    - Single comprehensive dashboard with complete page title, HTML, CSS, and JavaScript
                    - Full utilization of provided UI descriptors and CSS styling
                    - Implementation of selected layout structure with enhancements
                    - Professional, production-ready code suitable for business use"""
                ),
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
