# 🧬 Bically: The Hybrid Memory Orchestrator
> **Project Philosophy**: Logic is immutable; Personality is fluid. 

## 1. Project Version: 1.9.1-alpha (Refactor: Decoupled Logic)
This version marks the transition from hardcoded system prompts to a **Template-Driven Architecture**.

## 2. The Core Architecture (Decoupled RAG)
Bically is built on the **"Triangle of Truth"** principle. To maintain high-precision performance, we strictly separate three distinct layers:

* **The Engine (`main.py`)**: The orchestrator. It handles API calls, loops, and security.
* **The Memory (`vectordb.py` + Pinecone)**: The long-term episodic storage.
* **The Persona (`templates/orchestrator.xml`)**: The identity layer. This is where the AI's "soul" lives.

## 3. The Template Engine (`prompt_loader.py`)
Innovation: Instead of using Python f-strings, Bically now uses a dedicated loader to:
1. Read `templates/orchestrator.xml`.
2. Inject `{{ context }}` retrieved from Pinecone.
3. Inject `{{ version }}` from the global state.

## 4. The Identity Protocol (The "Kate" Rule)
The system solves the "Identity Paradox" by treating user names as **Dynamic Attributes**:
- **Protocol**: Never hardcode user identity in Python. 
- **Resolution**: Identity is retrieved via RAG. If "Kate" is found in the memory stream, Bically adopts that context immediately without code modification.

## 5. Instructions for AI Collaborators
- **Stateless Prompts**: Do not add text to `main.py`. Edit `templates/orchestrator.xml` instead.
- **RAG Consistency**: Always ensure `vectordb.py` uses the `<ENTRY>` schema for consistency.
