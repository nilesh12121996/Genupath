from langgraph.graph import StateGraph, END
from src.orchestrator.state import ApplicationState
from src.agents.sourcing_scout import sourcing_scout_node
from src.agents.intel_analyst import intel_analyst_node
from src.agents.resume_architect import resume_architect_node

def build_orchestrator():
    # Initialize the graph with the state schema
    workflow = StateGraph(ApplicationState)

    # Register the nodes (Agents)
    workflow.add_node("sourcing", sourcing_scout_node)
    workflow.add_node("intel_h1b", intel_analyst_node)
    workflow.add_node("resume_builder", resume_architect_node)

    # Define the routing logic
    workflow.set_entry_point("sourcing")
    workflow.add_edge("sourcing", "intel_h1b")
    
    # Conditional logic: Only build resume if H1B score is > 70
    def check_h1b_viability(state: ApplicationState):
        if state.get("h1b_probability_score", 0) > 70.0:
            return "resume_builder"
        return "end"

    workflow.add_conditional_edges(
        "intel_h1b",
        check_h1b_viability,
        {
            "resume_builder": "resume_builder",
            "end": END
        }
    )

    workflow.add_edge("resume_builder", END)

    return workflow.compile()
