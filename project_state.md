# 📍 Project State: AI Cloud Controller
**Date:** 2026-01-26
**Current Version:** 1.2.0 (Metadata Stamper Update)

---

## 🎯 1. Project Goal
Building a modular Python RAG (Retrieval-Augmented Generation) orchestrator. The system must ensure **Reasoning Traceability** (capturing DeepSeek-R1 thought blocks) and **Long-Term Memory** using Mixedbread AI with a custom Metadata Stamper logic.

---

## 🛠️ 2. Technical Stack & Environment
- **Runtime:** Python 3.10+
- **APIs:** Nebius AI (LLM), Mixedbread AI (Vector DB/Embeddings)
- **Architecture:** Modular Controller Pattern
- **Key Safety:** Credentials stored in external `.key` files, referenced by `config.json`.
- **Git State:** Current work is committed to `main` branch. `.gitignore` is active for keys and logs.

---

## 📂 3. Finalized File Registry
| File | Status | Core Responsibility |
| :--- | :--- | :--- |
| `main.py` | **STABLE** | CLI Controller. Handles `--trace`, `--dry-run`, and `!cat` commands. |
| `vectordb.py` | **STABLE** | Memory Module. Implements `get_mxb_client` with crash-safety and Metadata Stamper. |
| `logger.py` | **STABLE** | Audit Module. Saves Reasoning/CoT blocks to `traceability_audit.txt`. |
| `config.json` | **STABLE** | Registry for models, file paths, and `store_id`. |
| `aiguide.md` | **ACTIVE** | Technical blueprint for AI context (Hierarchical purpose of code). |
| `ai.md` | **ACTIVE** | Architect's roadmap and feature wishlist. |

---

## 🚀 4. Latest Progress & Logic
1.  **Dry Run Implementation:** Added `--dry-run` flag to `main.py` to allow testing RAG flow and logging without spending LLM tokens.
2.  **Metadata Stamper:** Updated `save_response` to tag every cloud memory with `created_at`, `source_type` (category), and `app_version`.
3.  **Crash Resilience:** `get_mxb_client` now catches `FileNotFoundError` for keys, returning `None` instead of crashing the app.
4.  **Dynamic Categories:** User can change the metadata category in real-time using `!cat [name]`.

---

## 📋 5. Immediate Next Steps
- [ ] Perform a live end-to-end test (without `--dry-run`) to verify Nebius API connection.
- [ ] Verify that `traceability_audit.txt` correctly captures the "Thinking" block from DeepSeek-R1.
- [ ] Explore Mixedbread filtering (using the stamped metadata to narrow down searches).

---

## 🧠 6. AI Context Injection
*When starting a new session, please refer to `aiguide.md` for function-level details. All key-loading must follow the `get_mxb_client` pattern (reading file paths from config, not raw keys).*
