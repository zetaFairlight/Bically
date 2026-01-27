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
