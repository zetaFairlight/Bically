# 🏛️ Bically Technical Specification & System Map
**Version:** v1.9.0-alpha (Hybrid Vector Pipeline)  
**Last Updated:** 2026-01-28  
**Status:** Alpha / Work-in-Progress

---

## 1. 🧩 Core Concepts & Philosophy

### 1.1 Structured XML Orchestration (Anthropic-Standard)
To solve "Instruction Bleed," Bically wraps the system payload in strictly delimited XML tags:
- **`<IDENTITY>`**: Hard-codes the persona, preventing "as an AI model" disclaimers.
- **`<KNOWLEDGE_BASE>`**: Dynamically holds retrieved Cloud memories.
- **`<CONSTRAINTS>`**: Injects behavioral rules such as conciseness and tone.

### 1.2 Hybrid Memory (Retrieval-Augmented Generation)
Bically uses a decoupled "Suitcase" approach for high-fidelity context:
1. **Long-Term**: Semantic search using Mixedbread `mxbai-embed-large-v1` embeddings (1024-dim) stored in a Pinecone Serverless index.
2. **Short-Term**: A sliding window of the last 6 messages (3 turns) held in RAM for immediate continuity.
3. **Fail-Fast Safety**: Decoupled `startup_check.py` validates cloud handshakes before initialization.

---

## 2. 📂 Project Hierarchy & Filesystem

```text
ai_project/
├── startup_check.py        # [NEW] Pre-flight API & Index verification
├── main.py                 # Core Orchestrator & Logic Controller
├── vectordb.py             # Hybrid Memory Engine (MXB + Pinecone)
├── accounting.py           # Persistent Budgeting & Cost Calculation
├── config.json             # Pricing, budget, and persistent session state
├── local_memory.txt        # Structured XML interaction logs
└── RELEASE_NOTES.md        # Detailed version and architectural history
```

---

## 3. 🔄 System Logic Flow (The RAG Loop)

1. **Safety Handshake**: `startup_check.py` validates cloud credentials before any LLM calls.
2. **Retrieval**: `vectordb.py` embeds the query via Mixedbread and queries Pinecone.
3. **XML Assembly**: `main.py` builds the "Suitcase" using the structured XML tags.
4. **Inference**: LLM generates response and reasoning chains.
5. **Persistence**: Budget is calculated and `config.json` state is updated on disk after every turn.
6. **Hybrid Sync**: Interaction is logged locally as an XML `<ENTRY>` and synced to Pinecone.

---

## 4. 🛠️ Key Libraries & Environment

| Library | Purpose |
| :--- | :--- |
| `openai` | Universal API client for Nebius and Google Gemini. |
| `pinecone-client` | [NEW] SDK for vector storage and serverless retrieval (v6.0.0+). |
| `mixedbread-ai` | [NEW] SDK for generating high-quality 1024-dim embeddings. |
| `simple-term-menu` | Powers the TUI selection menus. |

---

## 📝 Developer Notes
* **Alpha Warning**: As of v1.9.0-alpha, the Pinecone index `bically-memory` is subject to schema resets.
* **State Logic**: `config.json` now acts as a persistent database for `current_session_spend`.
* **Secret Management**: Ensure `.pinecone_key` and `.mxbai_key` are present in the root directory.
