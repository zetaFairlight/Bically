# === FILE: DOCUMENTATION.md ===
# 🤖 Bically Technical Documentation (v1.9.0-alpha)

## 🏗️ System Architecture
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestrator** | `main.py` | Executes the RAG loop and enforces the "Fail-Fast" handshake. |
| **Safety Guard** | `startup_check.py` | [NEW] Verifies API keys and Pinecone index status before launch. |
| **Memory Engine** | `vectordb.py` | [UPDATED] Hybrid pipeline using Mixedbread (Embed) and Pinecone (Store). |
| **Accounting** | `accounting.py` | Calculates real-time USD costs and persists them to `config.json`. |

---

## ⚙️ Logic & Data Flow
1. **Safety Handshake**: `startup_check.py` validates cloud credentials to prevent partial session crashes.
2. **Retrieval**: `vectordb.py` embeds query via Mixedbread and performs a semantic search in Pinecone.
3. **Structuring**: `main.py` builds the XML "Suitcase" (`<IDENTITY>`, `<KNOWLEDGE_BASE>`, `<CONSTRAINTS>`).
4. **Inference**: LLM processes the structured context and generates a response.
5. **Stateful Sync**: Budget is updated in `config.json` and the interaction is synced to Pinecone with session metadata.

---

## 🛡️ Technical Guardrails
### 1. Structured Prompting (Anthropic Standard)
The system uses the following tag hierarchy for reliability:
- `<IDENTITY>`: Sets the Bically persona.
- `<KNOWLEDGE_BASE>`: Houses long-term context from Pinecone.
- `<CONSTRAINTS>`: Enforces behavioral rules.

### 2. Budgeting Logic
- **Persistence**: Unlike v1.5.5, the budget is now flushed to disk after every turn to ensure continuity across restarts.
- **Safety**: Hard-exit to prevent overspending beyond `max_usd` defined in `config.json`.

### 3. Connection Persistence
- **Pattern**: Singleton clients in `vectordb.py` for both Mixedbread and Pinecone prevent latency from repeated SSL handshakes.
