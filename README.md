# 🚀 AI Cloud Controller Operations Manual

## 🎮 Execution Commands
Run the system using the following CLI flags to override `config.json` settings:

| Flag | Description |
| :--- | :--- |
| `--trace` | **Traceability Mode**: Prints reasoning/CoT and logs to `traceability_audit.txt`. |
| `--dry-run` | **Safety Mode**: Mocks responses and forces local-only memory ($0 cost). |
| `--model [id]` | **Pre-select**: Skips initial navigation to a specific model. |

**Example:** `python3 main.py --trace --model nebius_deepseek_r1`

---

## 🧠 Smart Features
- **Budget Guard**: Automatically tracks token usage and enforces a hard USD stop (default $0.05).
- **Interactive Menu**: Edit your budget limit or switch models directly from the startup UI.
- **Local Persistence**: Conversations are always saved to `local_memory.txt`, even if cloud sync is disabled.

---

## 🛠️ Requirements & Setup
1. `pip install openai mixedbread-ai simple-term-menu`
2. Add API keys to your root: `.nebius_key`, `.mxbai_key`, `.gemini_key`.
3. Update `config.json` with your Mixedbread `store_id`.
