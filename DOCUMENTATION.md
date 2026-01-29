# 🧬 Bically DNA & Project Rules
**Version**: 1.9.2-alpha
**Focus**: Maintenance, Safety, and AI-Agent Guardrails

## 1. The Decoupling Protocol
This is the most critical rule for the v1.9.1 branch. To maintain an "Elegant 2026" architecture, we follow a strict **No-Static-Identity** policy:
* **Zero Identity Hardcoding**: Never write user names or specific persona traits directly into Python files.
* **RAG Primacy**: If the system needs to know "Who am I talking to?", it must look into the `{{ context }}` provided by the database.
* **Template Isolation**: All modifications to Bically's tone, brevity, or constraints MUST happen in `templates/orchestrator.xml`.

## 2. Operational Safety
* **Pre-Flight Checks**: The `startup_check.py` must run at every launch to verify that Mixedbread and Pinecone API keys are valid and the cloud index is online.
* **Fail-Fast Mechanism**: If any dependency (Mixedbread, Pinecone, or Config) is missing, the system must `sys.exit(1)` immediately to prevent data corruption.

## 3. Developer & AI Assistant Rules
* **Version Consistency**: When updating the code, ensure `APP_VERSION` in `main.py` matches the headers in this file.
* **Schema Protection**: Do not change the metadata structure in `vectordb.py` without updating the search logic. The system expects a `text` field containing the interaction log.
* **Accounting**: Every completion must be logged through the `accounting.py` module to ensure session budgets are respected.

## 4. Troubleshooting
- **Identity Confusion**: If Bically forgets a name, check the Pinecone index to ensure the `<ENTRY>` tags are being synced correctly by `save_response`.
- **Loading Errors**: If the system prompt fails, verify that `templates/orchestrator.xml` exists and is readable.
