# 🚀 AI Cloud Controller Operations Manual

## 🎮 Execution Commands
Run the system using the following CLI flags to override `config.json` settings:

| Flag | Description |
| :--- | :--- |
| `--trace` | **Traceability Mode**: Prints the AI's internal "thinking" and logs to audit. |
| `--dry-run` | **Safety Mode**: Mocks responses and forces local-only memory (zero cost). |
| `--model` | **Pre-select**: Skips initial navigation to a specific model. |

**Example:** `python3 main.py --trace --model nebius_deepseek_r1`

---

## 🧠 Integrated Models & Budgeting
- **DeepSeek-R1**: High-reasoning with full Chain of Thought (CoT) capture.
- **DeepSeek-V3**: High-speed efficiency for general tasks.
- **Budget Guard**: Automatically tracks token usage and enforces a hard USD stop.

## 🛠️ Setup
1. `pip install openai mixedbread-ai simple-term-menu`
2. Add `.nebius_key` and `.mxbai_key` to your root directory.
3. Update `config.json` with your Mixedbread `store_id`.
