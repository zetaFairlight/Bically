# 🤖 Bically Technical Documentation (v1.5.5)

## 🏗️ System Architecture
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestrator** | `main.py` | Assembles the Structured XML payload and executes the RAG loop. |
| **UI Module** | `menu.py` | Interactive model & budget management via `simple-term-menu`. |
| **Memory Engine** | `vectordb.py` | Persistent Vector Retrieval with Singleton client for Mixedbread AI. |
| **Audit Chain** | `logger.py` | Records CoT (Chain of Thought) reasoning paths. |

---

## ⚙️ Logic & Data Flow
1. **Input**: User enters query.
2. **Retrieval**: `search_memories()` pulls the top matches from the Cloud.
3. **Structuring**: `main.py` wraps identity, context, and rules into a single `<SYSTEM_PROMPT>` block using XML delimiters.
4. **Inference**: LLM processes the structured "Suitcase."
5. **Structured Sync**: Interaction is logged locally as an XML `<ENTRY>` and synced to Cloud.

---

## 🛡️ Technical Guardrails
### 1. Structured Prompting (Anthropic Standard)
The system uses the following tag hierarchy for reliability:
- `<IDENTITY>`: Sets the Bically persona.
- `<KNOWLEDGE_BASE>`: Houses long-term context from Mixedbread.
- `<CONSTRAINTS>`: Enforces behavioral rules.

### 2. Budgeting Logic
- **Formula**: `(input_tokens / 1M * rate) + (output_tokens / 1M * rate)`.
- **Safety**: Hard-exit via `sys.exit(0)` to prevent overspending.

### 3. Connection Persistence
- **Pattern**: Singleton client in `vectordb.py` prevents SSL re-negotiation latency.
- **Manual Refresh**: `get_mxb_client(force_refresh=True)` allows resetting the connection if keys change.
