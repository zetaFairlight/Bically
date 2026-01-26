# 🤖 System Architecture

## 🏗️ Technical Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **UI Module** | `simple-term-menu` | Interactive model & budget management |
| **Budget Engine** | Custom Tracker | Real-time USD cost calculation & hard-stops |
| **Memory Engine** | Mixedbread AI | Cloud-first Contextual Retrieval (RAG) |
| **Versioning** | Git (Local) | Secure, offline version tracking with `.gitignore` |

---

## ⚙️ Logic Flow
1. **Recall**: Retrieves top 3 context matches from Mixedbread Cloud.
2. **Inference**: LLM generates a response using context; captures reasoning for DeepSeek-R1.
3. **Audit**: `check_budget()` calculates cost and logs "thoughts" to `traceability_audit.txt`.
4. **Sync**: Saves the answer to Mixedbread Cloud and `local_memory.txt`.

---

## 📂 Core Modules
* **`main.py`**: The orchestrator. Executes the RAG loop and enforces the Budget Guard.
* **`menu.py`**: UI layer. Handles persistent model selection and live budget overrides.
* **`vectordb.py`**: Memory engine. Implements 2-step Cloud Sync (File -> Store).
* **`logger.py`**: Compliance layer. Captures reasoning for transparency.
