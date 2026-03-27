# CareerPilot: Technical Architecture Deep-Dive

This document provides a low-level technical breakdown of the **CareerPilot** autonomous job application ecosystem. While the main README provides a high-level overview, this document explores the state machines, data flow, and internal logic of each specific component.

---

## A. Workflow Orchestrator: The Central Brain

The heart of the system is a **Global State Manager** built on **LangGraph**. Unlike a simple script, this is a state machine that ensures data consistency across the entire application lifecycle.

![Workflow Orchestrator](./architecture/orchestrator-state.png)

* **State Machine:** Manages transitions (e.g., `Job Discovered` → `Verified H1B` → `Submitted`).
* **Robust Error Recovery:** If a submission fails due to a site timeout, the state manager allows the agent to retry without losing the generated resume or metadata.
* **Memory Management:** Queries the Polyglot Data Layer to load context, such as specific diversity question answers previously used for the same company.

---

## B. Agent Services Deep Dive

### 🔍 Agent 1: Sourcing Scout (The Scraping Pipeline)
This agent is a complex ETL pipeline designed for high-speed discovery.

![Sourcing Scout](./architecture/sourcing-scout-pipeline.png)

* **Fleet Management:** Orchestrates multiple headless browsers to crawl career portals.
* **Parsing Engine:** Uses LLMs to transform messy, unstructured HTML/Text into a **Structured JSON Payload** (Role, Tech Stack, Salary, Visa Info).

### ⚖️ Agent 2: Intel Analyst (The H1B Intelligence Engine)
This agent acts as a decision gate to ensure time is only spent on roles with a high probability of sponsorship.

![Intel Analyst](./architecture/intel-analyst-rag.png)

* **Direct RAG:** Executes Retrieval-Augmented Generation queries against the **USCIS H1B Data Hub**.
* **Sponsorship Probability Score:** Calculates a decisive score based on the company's historical approval data, filtering out low-probability roles before they reach the Architect phase.

### 📝 Agent 3: Resume Architect (Content & Formatting Sandbox)
A sophisticated content engine that goes beyond simple keyword stuffing.

![Resume Architect](./architecture/resume-architect-sandbox.png)

* **Tailsmithing Engine:** Rewrites experience bullets to match JD requirements using **Strict Bolding** of technical expertise.
* **LaTeX Engine:** Compiles content into a clean, aesthetic PDF.
* **ATS Parser Simulation:** Before saving, the PDF is passed through a simulated ATS parser to ensure a **Match Score ≥ 90%**.

### 🚀 Agent 4: Submission Pilot (The RPA Executioner)
This agent handles the heavy lifting of form interaction through Robotic Process Automation.

![Submission Pilot](./architecture/submission-pilot-rpa.png)

* **Computer Vision / DOM Analysis:** Navigates portals like Workday, Greenhouse, and Taleo.
* **Anti-Bot Emulation:** Uses logic to introduce random human-like delays, varied mouse movements, and natural typing speeds to bypass detection.

### 🤝 Agent 5: Networking Agent (Post-Application CRM)
Closes the loop by automating professional outreach.

![Networking Agent](./architecture/networking-agent-crm.png)

* **Graph Traversal:** Uses social graphs to identify the specific recruiter or hiring manager for the role.
* **Personalized LLM Outreach:** Generates non-generic connection requests that reference the specific application and the candidate's unique technical fit.

---

## C. Data Layer: Polyglot Persistence

We use a "Right Tool for the Job" approach to storage to ensure auditability and performance.

![Data Layer](./architecture/data-layer-polyglot.png)

| Storage Type | Technology | Purpose |
| :--- | :--- | :--- |
| **Structured Jobs DB** | PostgreSQL | Metadata, salary ranges, and sponsorship scores. |
| **Resume/File Storage** | AWS S3 | Exact archival of every tailored PDF for full traceability. |
| **Application Logs** | ELK/Datadog | Submission IDs, timestamps, and bot performance monitoring. |

---