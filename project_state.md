# 📍 Project State: AI Cloud Controller
**Date:** 2026-01-26
**Current Version:** 1.3.0 (Total Dry Mode & SDK Alignment)

---

## 🎯 1. Project Goal
Building a modular Python RAG (Retrieval-Augmented Generation) orchestrator. The system must ensure **Reasoning Traceability** (capturing DeepSeek-R1 thought blocks) and **Long-Term Memory** using Mixedbread AI with a custom Metadata Stamper logic.

---

## 🛠️ 2. Technical Stack & Environment
- **Runtime:** Python 3.10+
- **APIs:** Nebius AI (LLM), Mixedbread AI (Vector DB/Embeddings)
- **Architecture:** Modular Controller Pattern
- **Key Safety:** Credentials stored in external `.key` files, referenced by `config.json`.

---

## 📂 3. Finalized File Registry
| File | Status | Core Responsibility |
| :--- | :--- | :--- |
| `main.py` | **STABLE** | CLI Controller. Now features **Total Dry Mode** to skip all API costs. |
| `vectordb.py` | **STABLE** | Memory Module. Implements 2-step Mixedbread upload (File -> Store) and metadata stamping. |
| `logger.py` | **STABLE** | Audit Module. Saves Reasoning/CoT blocks to `traceability_audit.txt`. |
| `config.json` | **STABLE** | Registry for models, file paths, and `store_id`. |
| `aiguide.md` | **ACTIVE** | Technical blueprint for AI context (Hierarchical purpose of code). |

---

## 🚀 4. Latest Progress & Logic
1.  **Total Dry Mode:** Updated `--dry-run` in `main.py` to block both LLM tokens and Mixedbread search/save units by forcing `local` mode.
2.  **SDK Alignment:** Fixed `vectordb.py` to use a two-step process: `client.files.create` followed by `client.stores.files.create` to match Mixedbread SDK requirements.
3.  **Crash Resilience:** `get_mxb_client` handles missing key files gracefully, returning `None` instead of crashing.
4.  **Metadata Stamper:** All cloud saves include `created_at` and `source_type` (category) metadata.

---

## 📋 5. Immediate Next Steps
- [ ] Perform a live end-to-end test (without `--dry-run`) to verify Nebius and Mixedbread API connections.
- [ ] Verify that `traceability_audit.txt` correctly captures the "Thinking" block from DeepSeek-R1.

---

## 🧠 6. AI Context Injection
*Refer to `aiguide.md` for function-level details. All key-loading follows the `get_mxb_client` pattern.*
