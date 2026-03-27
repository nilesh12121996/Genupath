from src.orchestrator.state import ApplicationState

def sourcing_scout_node(state: ApplicationState) -> ApplicationState:
    print("[Agent 1] Sourcing Scout: Scraping Job Description...")
    state["audit_logs"].append("Scraped JD successfully.")
    state["current_status"] = "JD_PARSED"
    return state
