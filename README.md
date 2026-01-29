# 🚀 Bically AI v1.9.2-alpha

Bically is a high-precision AI orchestrator. This version marks the transition to a **Decoupled Template Architecture**, where the AI's persona is separated from the execution engine.

## 🛠 Quick Start
1. **Safety Check**: Run `python main.py` to trigger the automated `startup_check.py`.
2. **Dynamic Persona**: Edit `templates/orchestrator.xml` to change Bically's tone or rules. 
3. **Execution**: Use `--trace` to see the new decoupled prompt assembly in action.

## 🧩 v1.9.1 Refactor Highlights
- **Engine/Persona Split**: Python code no longer contains identity strings or long XML prompts.
- **Template Injection**: Uses `prompt_loader.py` to hydrate XML with RAG context.
- **Identity Fluidity**: User names (e.g., "Kate") are now dynamic RAG attributes.
