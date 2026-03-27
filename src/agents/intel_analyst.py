from src.orchestrator.state import ApplicationState

def intel_analyst_node(state: ApplicationState) -> ApplicationState:
    print("[Agent 2] Intel Analyst: Checking H1B Sponsorship Probability...")
    # Mocking a high score for testing
    state["h1b_probability_score"] = 92.5 
    state["audit_logs"].append(f"H1B score calculated: {state['h1b_probability_score']}")
    return state
