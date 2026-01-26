# 🤖 System Architecture

## 🏗️ Technical Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **UI Module** | `simple-term-menu` | Interactive model & budget management |
| **Budget Engine** | Custom Tracker | Real-time USD cost calculation & hard-stops |
| **Memory Engine** | Mixedbread AI | Cloud-first Contextual Retrieval (RAG) |
| **Versioning** | Git (Local) | Secure, offline version tracking with `.gitignore` |

---
# 🤖 System Architecture

## 📂 Core Modules
* **`main.py`**: The orchestrator. Executes the RAG loop, intercepts commands like `/menu`, and enforces the Budget Guard.
* **`menu.py`**: UI layer. Handles persistent model selection and live budget overrides.
* **`vectordb.py`**: Memory engine. Implements 2-step Cloud Sync (File -> Store).
* **`logger.py`**: Compliance layer. Captures reasoning blocks for transparency.

## ⚙️ Logic Flow
1. **Search**: Retrieves top 3 context matches from Mixedbread.
2. **Command Intercept**: Checks if user input is `/menu` to re-initialize the provider and API client.
3. **Inference**: LLM generates response using context + reasoning.
4. **Audit**: `check_budget()` calculates USD cost and logs "thoughts" to `traceability_audit.txt`.
5. **Sync**: Saves the answer to Cloud and `local_memory.txt`.

---

## 📂 Core Modules
* **`main.py`**: The orchestrator. Executes the RAG loop, intercepts commands like `/menu`, and enforces the Budget Guard.
* **`menu.py`**: UI layer. Handles persistent model selection and live budget overrides.
* **`vectordb.py`**: Memory engine. Implements 2-step Cloud Sync (File -> Store).
* **`logger.py`**: Compliance layer. Captures reasoning blocks for transparency.
