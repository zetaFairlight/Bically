# 🗺️ BICAL TECHNICAL SPECIFICATION
**Version**: 1.9.2-alpha
**Status**: Decoupled RAG Implementation Complete

## 1. Architectural Overview: The Decoupled Suitcase
In version 1.9.1, Bically moves from a monolithic prompt structure to a **Suitcase Assembly Model**. The "Personality" and "Identity" of the AI are treated as external data packets rather than hardcoded logic.

## 2. Component breakdown
* **The Orchestrator (`main.py`)**: Responsible for session management, token accounting via `accounting.py`, and the primary chat loop.
* **The Memory Engine (`vectordb.py`)**: Uses Mixedbread AI for high-dimensional embeddings and Pinecone for vector storage.
* **The Bridge (`prompt_loader.py`)**: A new utility that reads XML templates and performs variable injection.
* **The Asset (`templates/orchestrator.xml`)**: The single source of truth for Bically's behavior and constraints.

## 3. The Retrieval-Augmented Generation (RAG) Flow
1.  **Input Vectorization**: User input is converted into a vector using the `mixedbread-ai/mxbai-embed-large-v1` model.
2.  **Semantic Search**: Pinecone is queried for the `top_k` most relevant historical entries.
3.  **Template Hydration**: `prompt_loader.py` retrieves the XML and replaces the `{{ context }}` placeholder with the retrieved memories.
4.  **Final Inference**: The hydrated system prompt is sent to the LLM (DeepSeek/Nebius).

## 4. Data Persistence
All interactions are wrapped in `<ENTRY>` tags and synced to the cloud index with unique UUIDs and timestamps. This ensures that identity markers (like the name "Kate") are persistent across sessions without being hardcoded.
