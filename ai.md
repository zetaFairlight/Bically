# 🤖 System Architecture

## 📂 Core Modules
* **`main.py`**: The orchestrator. Executes the RAG loop and enforces the Budget Guard.
* **`menu.py`**: UI layer. Handles persistent model selection and live budget overrides.
* **`vectordb.py`**: Memory engine. Implements 2-step Cloud Sync (File -> Store).
* **`logger.py`**: Compliance layer. Captures reasoning for transparency.

## ⚙️ Logic Flow
1. **Search**: Retrieves top 3 context matches from Mixedbread.
2. **Inference**: LLM generates response using context + reasoning.
3. **Audit**: Calculates USD cost and logs "thoughts" to `traceability_audit.txt`.
4. **Sync**: Saves the answer to Cloud and `local_memory.txt`.
