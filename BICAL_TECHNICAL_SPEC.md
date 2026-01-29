This new file, **`BICAL_TECHNICAL_SPEC.md`**, acts as the definitive "master map" of your project. It consolidates every logic change we’ve made up to **v1.5.5**, including the granular function details, the new XML-structured memory patterns, and the environment setup.

### 📄 BICAL_TECHNICAL_SPEC.md

```markdown
# 🏛️ Bically Technical Specification & System Map
**Version:** v1.9.0-alpha (Hybrid Memory Decoupling)  
**Last Updated:** 2026-01-27 10:30:00  
**Status:** Operational / Lean Documentation Mode  

---

## 1. 🧩 Core Concepts & Philosophy

### 1.1 Structured XML Orchestration (Anthropic-Standard)
To solve "Instruction Bleed" (where the AI confuses data with commands), Bically wraps the system payload in strictly delimited XML tags. 
- **`<IDENTITY>`**: Hard-codes the persona, preventing "as an AI model" disclaimers.
- **`<KNOWLEDGE_BASE>`**: Dynamically holds retrieved Cloud memories.
- **`<CONSTRAINTS>`**: Injects behavioral rules (conciseness, tone).

### 1.2 Hybrid RAG (Retrieval-Augmented Generation)
Bically uses a "Suitcase" approach for context:
1. **Long-Term**: Semantic search via Mixedbread AI (Cloud).
2. **Short-Term**: A sliding window of the last 6 messages (3 turns) held in RAM.
3. **Local Sync**: Parallel XML logging to `local_memory.txt`.

---

## 2. 📂 Project Hierarchy & Filesystem

```text
ai_project/
├── .venv/                  # Python 3.10+ Virtual Environment
├── .nebius_key             # [SECRET] Nebius AI API Key
├── .mxbai_key              # [SECRET] Mixedbread AI API Key
├── .gemini_key             # [SECRET] Google Gemini API Key
├── config.json             # Provider pricing, models, and budget limits
├── last_model.json         # State persistence for model selection
├── main.py                 # Core Orchestrator & Logic Controller
├── vectordb.py             # Memory Engine & Cloud Sync Module
├── menu.py                 # Interactive TUI selection & Budget Editor
├── logger.py               # Traceability & Reasoning Logger
├── local_memory.txt        # Structured XML interaction logs
├── traceability_audit.txt  # Chain-of-Thought (CoT) reasoning logs
└── DOCUMENTATION.md        # Unified user-facing technical guide

```

---

## 3. ⚙️ Module & Function Breakdown

### 3.1 `main.py` (The Brain)

The central controller managing the interaction loop and API assembly.

* **`check_budget(usage, model_id, config)`**:
* Calculates real-time USD cost: `(Input/1M * Rate) + (Output/1M * Rate)`.
* Performs a `sys.exit(0)` hard-stop if `max_usd` is reached.


* **`main()`**:
* Handles CLI flags (`--trace`, `--dry-run`).
* Orchestrates the **XML System Message** construction.
* Manages `chat_history` (Short-term memory buffer).
* Intercepts `/menu` to trigger re-configuration.



### 3.2 `vectordb.py` (The Memory)

Interfaces with Mixedbread AI and manages local persistent logs.

* **`get_mxb_client(force_refresh)`**: **Singleton Pattern**. Reuses one client instance to prevent SSL latency.
* **`search_memories(query, top_k)`**: Retrieves top semantic matches. Handles nested `ScoredTextInputChunk` objects.
* **`save_response(text, mode)`**:
* **Remote**: 2-step process (Upload File -> Attach to Store).
* **Local**: Appends to `local_memory.txt` using the new `<ENTRY>` XML format.



### 3.3 `menu.py` (The UI)

Built on `simple-term-menu` for terminal interactivity.

* **`select_model_interactive()`**:
* Persistence: Reads/Writes `last_model.json`.
* Dynamic: Allows the user to edit the `max_usd` budget limit mid-session.



### 3.4 `logger.py` (The Auditor)

* **`log_trace()`**: Extracts `reasoning_content` (for DeepSeek-R1) or CoT and saves it with a high-res timestamp to `traceability_audit.txt`.

---

## 4. 🔄 System Logic Flow (The RAG Loop)

1. **User Input**: Query captured in `main.py`.
2. **Context Retrieval**: `vectordb.py` searches Cloud Memory for relevant history.
3. **XML Assembly**: `main.py` builds the "Suitcase":
* `[System Message]`: Structured XML (Identity + Context + Constraints).
* `[Chat History]`: Last 6 messages for immediate continuity.
* `[User Input]`: The current query.


4. **Inference**: LLM generates the response + Reasoning (if supported).
5. **Budget Check**: Cost is calculated and `config.json` state is updated.
6. **Dual-Sync**:
* Interaction synced to Mixedbread Cloud.
* Interaction saved to `local_memory.txt` as an XML `<ENTRY>`.


7. **Traceability**: Reasoning chains logged to `traceability_audit.txt` (if `--trace` active).

---

## 5. 🛠️ Key Libraries & Environment

| Library | Purpose |
| --- | --- |
| `openai` | Universal API client for Nebius and Google Gemini. |
| `mixedbread-ai` | SDK for vector search and cloud document management. |
| `simple-term-menu` | Powers the TUI selection menus. |
| `argparse` | Manages CLI flags like `--dry-run`. |

---

## 📝 Important Developer Notes

* **Log Formatting**: As of v1.5.5, all logs are **XML-formatted**. Do not use pipe-delimited strings for future features.
* **Secret Management**: Never commit `.*_key` files. Use the `.gitignore` provided in `DOCUMENTATION.md`.
* **Dry Run Safety**: In `--dry-run`, no cloud sync occurs, and the response is a mock string to preserve credits.

```

<LATEST_ARCHITECTURE_SHIFT>
  <FILE name="startup_check.py">
    <INTENT>Pre-flight safety; verifies API/Cloud before main loop.</INTENT>
  </FILE>
  <FILE name="vectordb.py">
    <INTENT>Decoupled logic: MXB for Embeddings, Pinecone for Storage.</INTENT>
  </FILE>
</LATEST_ARCHITECTURE_SHIFT>
