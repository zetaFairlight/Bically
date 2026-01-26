# 🤖 System Architecture (v1.5.1)

## 🏗️ Technical Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **UI Module** | `simple-term-menu` | Interactive model & budget management |
| **Budget Engine** | Custom Tracker | Real-time USD cost calculation & hard-stops |
| **Memory Engine** | Mixedbread AI | Persistent Vector Retrieval (RAG) |
| **Versioning** | Git (Local) | Secure, offline version tracking with `.gitignore` |

---

## 📂 Core Modules
* **`main.py`**: The orchestrator. Executes the RAG loop, intercepts `/menu`, and enforces Budget Guards.
* **`menu.py`**: UI layer. Handles persistent model selection and live budget overrides.
* **`vectordb.py`**: Memory engine. Implements persistent client and 2-step Cloud Sync (File -> Store).
* **`logger.py`**: Compliance layer. Captures reasoning blocks for transparency.

---

## ⚙️ Logic Flow
1. **Input**: User enters query or the `/menu` command.
2. **Command Intercept**: If `/menu`, re-run `menu.py` and re-initialize the `OpenAI` client.
3. **Search**: `vectordb.py` uses the persistent connection to retrieve top 3 context matches.
4. **Inference**: LLM generates response using injected context and reasoning.
5. **Audit**: `check_budget()` calculates cost and logs "thoughts" to `traceability_audit.txt`.
6. **Sync**: Saves the answer to Cloud and `local_memory.txt`.
