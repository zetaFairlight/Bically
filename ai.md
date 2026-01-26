# 🤖 System Architecture: AI Cloud Controller

## 🏗️ Technical Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestrator** | Python 3.10+ / OpenAI SDK | Logic, CLI Handling & API Routing |
| **LLM Hub** | Nebius AI (Blackwell/H800) | High-performance inference (NVIDIA/DeepSeek) |
| **Memory Engine** | Mixedbread AI (Cloud) | Contextual Retrieval (RAG) & Metadata Storage |
| **Audit Engine** | logger.py | Regulatory Traceability & Thought Logging |

---

## 📂 Core Modules & Purpose
* **`main.py`**: The central brain. Executes the **RAG (Retrieve-Augmented-Generate)** loop.
* **`vectordb.py`**: The memory middleware. Manages remote cloud stores and local fallback logs.
* **`logger.py`**: The compliance layer. Captures and timestamps the "Chain of Thought" (CoT).
* **`config.json`**: The system registry for API keys, model endpoints, and global flags.

---

## ⚙️ Core Logic & Feature Set

### 1. The RAG Loop (Contextual Retrieval)
The system enhances every query by pulling past "memories" before the LLM generates a response:
- **Search**: `search_memories()` finds the top 3 most relevant previous answers.
- **Augment**: These snippets are injected into the system prompt as "Context."
- **Generate**: The LLM uses the context to ensure factual accuracy and continuity.

### 2. Regulatory Traceability (DeepSeek-R1)
Specifically designed for countries with emerging AI transparency laws:
- **Reasoning Capture**: Extracts the `reasoning_content` field from DeepSeek-R1 responses.
- **Audit Logging**: Saves the user's question, the AI's internal "thinking" steps, and the final answer to `traceability_audit.txt` with UTC timestamps.

### 3. Metadata Stamper & Dynamic Categorization
Every memory saved to the cloud is enriched with metadata for better future retrieval:
- **Auto-Stamping**: Attaches `created_at`, `source_type`, and `app_version` tags.
- **Dynamic Switch**: Users can change the "Source Category" on the fly using the `!cat [Name]` command in the chat.
- **CLI Initialization**: The `--cat` flag sets the starting category (e.g., `python3 main.py --cat Finance`).

---

## 🎮 CLI Reference & Commands
| Command/Flag | Type | Effect |
| :--- | :--- | :--- |
| `--trace` | CLI Flag | Enables visual "thinking" blocks and audit logging. |
| `--local` | CLI Flag | Forces system to bypass Cloud and use `local_memory.txt`. |
| `--cat [Name]` | CLI Flag | Sets the initial storage category for the session. |
| `!cat [Name]` | In-Chat | Changes the category for all subsequent memories in the session. |
| `exit` | In-Chat | Safely closes the session. |

---

## 🛡️ Security & Versioning
- **Git Branching**: Main branch represents the current "Known Good" version.
- **Credential Protection**: `.gitignore` prevents `.key` files from being committed.
- **File Permissions**: Recommended `chmod 600` for all `.key` files.
