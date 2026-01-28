# 📝 Release Notes & Progress Log

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

## [v1.9.0-alpha] - 2026-01-28
### 🏗️ The Hybrid Memory Shift
This version moves away from Mixedbread's internal storage in favor of a **Mixedbread + Pinecone** hybrid pipeline. 

#### 🧩 For AI/Copilot Agents:
- **New Vector Flow**: Text -> `mxbai-embed-large-v1` -> Pinecone Index.
- **SDK Update**: Switched to `pinecone-client` v6.0.0+.
- **State Logic**: `config.json` now acts as a persistent DB for `current_session_spend`. 
- **Metadata**: Pinecone records now include `text` and `session_id` as primary metadata keys.
