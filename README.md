# 🛡️ AlertGuard-Ops: GitOps Alert Governance & Automated Cataloging

An enterprise-grade, GitOps-driven alerting governance engine that programmatically eliminates alert fatigue by enforcing data quality standards, automating ingest compliance, and generating an auto-updating centralized response catalog.

## 🎯 Business Context & Problem Statement
In large-scale enterprise environments, unmanaged monitoring configurations lead to systemic alert fatigue, causing 24x7 response teams to miss true, high-impact incidents. 

`AlertGuard-Ops` acts as an automated gatekeeper. It shifts alert configuration left into code (YAML), forcing service teams to meet strict "Definitions of Done" (such as mandatory metadata, verified service ownership, and documented triage steps) before an alert can ever be routed to operations.

## 🛠️ Framework Architecture & Core Tech Stack
* **Pipeline Automation:** GitHub Actions (CI/CD linting and compliance gate).
* **Governance Engine:** Python 3.10 (Object-oriented validation and configuration parsing).
* **State Persistence:** SQLite (Relational metadata asset tracking using an idempotent UPSERT pattern).
* **Documentation Automation:** Dynamic Markdown Compilation (Ensures 0% documentation drift).

## 📊 Mapping to Enterprise Deliverables (First 45 Days)

| JD Required Deliverable | Technical Implementation | Operational Outcome |
| :--- | :--- | :--- |
| **Establish Intake & Approval Workflow** | GitHub Actions Pipeline workflow automation gate. | Blocks non-compliant alerts at the Pull Request phase before reaching production monitoring systems. |
| **Enforce Alerting Standards & Routing** | Strict global schema configuration (`config/alerting_policy.yaml`). | Validates severity definitions, correct routing boundaries, and metadata tagging rules. |
| **Mandate Response Instructions (Runbooks)** | Comprehensive triage checklist schema enforcement. | 100% of alerts routed to 24x7 Operations are guaranteed to include actionable triage steps and escalation triggers. |
| **Create Central Alert Catalog** | Dynamic SQLite relational backend mapping to auto-compiled `CENTRAL_ALERT_CATALOG.md`. | Delivers a single, audited source of truth showing active service ownership and valid runbook links. |

## 🚀 Local Installation & Execution

### 1. Clone & Initialize Environment
```bash
git clone [https://github.com/dez84/alertguard-ops.git](https://github.com/dez84/alertguard-ops.git)
cd alertguard-ops
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Execute the Full Pipeline Loop
Run the central entry point script to validate localized definitions, ingest passing components, and compile the global documentation catalog:
python main.py

🛡️ Governance Enforcement Logs Example

================================================================
=== Launching AlertGuard-Ops CI/CD Integration Engine ===
================================================================

--- Starting Alert Guard Governance Scan (2 files found) ---
[DB] Central alert inventory successfully initialized at: /home/dez/alertguard-ops/alert_inventory.db
-----------------------------------------------------------------
[PASS] checkout_service_alerts.yaml: Alert definition meets corporate standards.
[DB LOG] Successfully archived/updated policy state for alert: 'Checkout_HTTP_5xx_Spike'

[FAIL] payment_service_alerts.yaml:
  - CRITICAL VIOLATION: Routes to '24x7_Eyes_on_Glass' but lacks a 'runbook_url'.
  - Insufficient operational impact description. Must be at least 15 characters.
-----------------------------------------------------------------

[FAILURE] Governance violations detected on incoming configurations.
=== Pipeline Execution Halted: Catalog Generation Skipped ===
