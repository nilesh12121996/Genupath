from typing import TypedDict, List, Dict, Any

class ApplicationState(TypedDict):
    job_url: str
    company_name: str
    jd_structured: Dict[str, Any]
    h1b_probability_score: float
    ats_match_score: float
    resume_pdf_path: str
    current_status: str
    audit_logs: List[str]
    errors: List[str]
