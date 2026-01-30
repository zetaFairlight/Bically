## [v1.9.1-patch] - 2026-01-29
### 🛠️ Maintenance
- Integrated XML-structured documentation for RAG precision.
- Added 'bz' and 'br' rapid-triggers.

# 📝 Release Notes & Progress Log

# 📝 Release Notes & Progress Log

## [v1.9.1-alpha] - 2026-01-28
### 🚀 The Hybrid Memory Shift (Work in Progress)
*This version introduces a major decoupling of our vector pipeline.*

#### 🧩 Core Architectural Changes:
- **Decoupled Pipeline**: Switched from Mixedbread-only storage to a **Mixedbread + Pinecone** hybrid. Mixedbread now handles the 1024-dim embeddings, while Pinecone Serverless manages the long-term retrieval.
- **Fail-Fast Safety (New)**: Integrated `startup_check.py` to verify API keys and cloud connectivity *before* the main orchestrator initializes. This prevents partial session crashes.
- **Persistent Budgeting**: Fixed a bug where session spend was only held in memory; `main.py` now flushes the USD balance to `config.json` after every interaction.

#### 📝 Minor Release Notes (Internal Agent Instructions):
- **SDK Migration**: All `pinecone-client` calls are deprecated. Use `pinecone-client` v6.0.0+.
- **Metadata Standard**: Every memory upsert now requires a JSON metadata block with `session_id`, `text`, and `timestamp`.
- **Alpha Warning**: As this is an ALPHA, the Pinecone index `bically-memory` is subject to schema resets.

## [v1.5.5] - 2026-01-27
### 🚀 Structured Orchestration (Current)
- **Structured XML Prompting**: Transitioned from flat system messages to a hierarchical XML payload.
- **XML Logging Standard**: Local logs now follow a machine-readable format (`<ENTRY>`, `<USER>`, `<AI>`).
- **Impact**: Dramatically improves accuracy when recalling personal facts and resolves context "amnesia."

## [v1.5.2] - 2026-01-26
### 🔄 Hybrid Memory & Statefulness
- **Hybrid Architecture**: Implemented a `chat_history` list in `main.py` for the last 6 message turns.
- **Indexing Mitigation**: Injecting the local buffer into the API payload provides immediate context before the Cloud DB finishes indexing.
- **Bug Fix**: `vectordb.py` now safely handles nested `content` attributes in Mixedbread search results.

## [v1.5.1] - 2026-01-26
### 🏗️ Initial Framework
- **Singleton Client**: Introduced persistent cloud connections for faster retrieval.
- **Budget Guard**: Implemented real-time token tracking and USD hard-stops.

#### 🧩 For AI/Copilot Agents:
- **New Vector Flow**: Text -> `mxbai-embed-large-v1` -> Pinecone Index.
- **SDK Update**: Switched to `pinecone-client` v6.0.0+.
- **State Logic**: `config.json` now acts as a persistent DB for `current_session_spend`. 
- **Metadata**: Pinecone records now include `text` and `session_id` as primary metadata keys.
