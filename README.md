# 🚀 Bically | v1.5.1 (Stateful Linear RAG)

**A high-precision terminal interface for multi-model interactions with integrated memory and budget safety.**

## 🎮 Execution Commands
Run the system using the following CLI flags to override `config.json` settings:

| Flag | Description |
| :--- | :--- |
| `--trace` | **Traceability Mode**: Prints the AI's internal "thinking" and logs to `traceability_audit.txt`. |
| `--dry-run` | **Safety Mode**: Mocks responses and forces local-only memory ($0 cost). |
| `--model [id]` | **Pre-select**: Skips initial navigation to a specific model. |

**Example**: `python3 main.py --trace --model nebius_deepseek_r1`

---

## ⌨️ In-Chat Commands
While the chat session is active, you can use these special commands:
- `/menu`: Re-opens the model selection menu to switch LLMs or edit the budget mid-session.
- `exit` or `quit`: Safely closes the session and updates the budget log.

---

## 🧠 Smart Features
- **Low-Latency Search**: v1.5.1 introduces persistent cloud connections (Singleton) for faster RAG retrieval.
- **Budget Guard**: Automatically tracks token usage and enforces a hard USD stop (default $0.05).
- **Interactive Menu**: Edit your budget limit or switch models directly from the startup UI or mid-chat.
- **Local Persistence**: Conversations are always saved to `local_memory.txt`, even if cloud sync is disabled.
- **Traceability**: Captured "Thinking" blocks saved to `traceability_audit.txt`.

---

## 🧠 Integrated Models & Budgeting
- **DeepSeek-R1**: High-reasoning with full Chain of Thought (CoT) capture.
- **DeepSeek-V3**: High-speed efficiency for general tasks.
- **Budget Guard**: Automatically tracks token usage and enforces a hard USD stop (default $0.05).

---

## 🛠️ Setup
1. `pip install openai mixedbread-ai simple-term-menu`.
2. Add API keys to your root: `.nebius_key`, `.mxbai_key`, `.gemini_key`.
3. Update `config.json` with your Mixedbread `store_id`.
