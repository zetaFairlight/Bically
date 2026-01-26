# 🤖 System Architecture: AI Cloud Controller

## 🏗️ Technical Stack
| Component | Technology | Role |
| :--- | :--- | :--- |
| **Orchestrator** | Python 3.10+ / OpenAI SDK | Logic, CLI Handling & API Routing |
| **LLM Hub** | Nebius AI (Blackwell/H800) | High-performance inference (NVIDIA/DeepSeek) |
| **Memory Engine** | Mixedbread AI (Cloud) | Contextual Retrieval (RAG) |
| **Audit Engine** | logger.py | Regulatory Traceability & Thought Logging |

---

## 📂 Core Modules & Purpose
* **`main.py`**: The central brain. It executes a **Retrieve-Augmented-Generate (RAG)** loop. It searches your cloud memory first, injects that context into the prompt, and then asks the LLM for a grounded answer.
* **`vectordb.py`**: The memory middleware. It handles both "Remote" (Cloud API) and "Local" (Simple text log) modes. It ensures your AI doesn't have "amnesia" between sessions.
* **`logger.py`**: The compliance layer. It captures the **Reasoning Content** (Chain of Thought) from models like DeepSeek-R1, saving it with UTC timestamps for future debugging or legal audits.
* **`config.json`**: The system registry. All API endpoints, model IDs, and security flags live here.

---

## ⚙️ Key Functionality: The Reasoning Loop
1.  **Retrieval**: System calls `search_memories()` in `vectordb.py`.
2.  **Augmentation**: Top-K context snippets are prepended to your query.
3.  **Inference**: The LLM processes the augmented prompt. If using a Reasoning model, the "Thought Block" is isolated.
4.  **Logging**: The Final Answer + Thoughts are saved to `traceability_audit.txt`.
