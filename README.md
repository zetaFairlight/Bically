# === FILE: README.md ===
# 🚀 Bically | v1.9.0-alpha (Hybrid Memory Orchestrator)

**A high-precision terminal interface for multi-model interactions with integrated XML-structured hybrid memory and budget safety.**

## 🛡️ Pre-Flight Safety
As of **v1.9.0-alpha**, the system executes `startup_check.py` automatically. It verifies your `.mxbai_key` and `.pinecone_key` and confirms the cloud index is online before initializing the chat.

## 🧠 Smart Features
- **Hybrid RAG Pipeline**: Decouples embeddings (Mixedbread) from storage (Pinecone) for unlimited scaling.
- **Structured XML Orchestration**: Maintains high-fidelity recall using tags like `<IDENTITY>` and `<KNOWLEDGE_BASE>`.
- **Persistent Budgeting**: Flushes USD balance to `config.json` after every interaction.

---

# === FILE: BICAL_TECHNICAL_SPEC.md ===
# 🏛️ Bically Technical Specification & System Map
**Version:** v1.9.0-alpha (Hybrid Vector Pipeline)

## 1. 🧩 Core Concepts
### 1.1 Hybrid Memory (RAG)
1. **Embedding (Mixedbread)**: Generates 1024-dimension vectors.
2. **Storage (Pinecone)**: Manages the vector database and semantic search.

## 2. 📂 Project Hierarchy
- `startup_check.py`: [NEW] Pre-flight API & Index verification.
- `vectordb.py`: Hybrid Memory Engine (MXB + Pinecone).
- `config.json`: Pricing, budget, and persistent session state.

---

# === FILE: RELEASE_NOTES.md ===
# 📝 Release Notes & Progress Log

## [v1.9.0-alpha] - 2026-01-28
### 🚀 The Hybrid Memory Shift (Work in Progress)
- **Decoupled Pipeline**: Switched to Mixedbread + Pinecone hybrid.
- **Fail-Fast Safety**: Integrated `startup_check.py` to prevent partial session crashes.
- **Persistent Budgeting**: Fixed bug where session spend was only held in memory.

## [v1.5.5] - 2026-01-27
### 🚀 Structured Orchestration
- **Structured XML Prompting**: Transitioned from flat messages to hierarchical XML.
- **XML Logging Standard**: Local logs now follow the machine-readable `<ENTRY>` format.
