from src.orchestrator.graph import build_orchestrator
from src.orchestrator.state import ApplicationState

def main():
    print("🚀 Initializing CareerPilot Orchestrator...")
    app_orchestrator = build_orchestrator()

    # Create a fresh job application state
    initial_state = ApplicationState(
        job_url="https://careers.google.com/jobs/12345",
        company_name="Google",
        jd_structured={},
        h1b_probability_score=0.0,
        ats_match_score=0.0,
        resume_pdf_path="",
        current_status="PENDING",
        audit_logs=["Job application initialized."],
        errors=[]
    )

    # Run the pipeline
    print("\n--- Starting Pipeline ---")
    final_state = app_orchestrator.invoke(initial_state)
    
    print("\n--- Pipeline Complete ---")
    print("\nFinal Application State:")
    for key, value in final_state.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
