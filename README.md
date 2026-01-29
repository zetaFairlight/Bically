<VERSION_LOG>
  <ID>v1.9.0-alpha</ID>
  <ARCH>Hybrid-Pinecone</ARCH>
</VERSION_LOG>

# 🚀 Bically | v1.9.0-alpha (Hybrid Pinecone RAG)

**A high-precision terminal interface for multi-model interactions with integrated XML-structured memory and budget safety.**

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
- **Structured XML Orchestration**: v1.5.5 utilizes industry-standard XML tags (`<IDENTITY>`, `<KNOWLEDGE_BASE>`) to ensure high-fidelity recall.
- **Low-Latency Search**: Persistent cloud connections (Singleton) for faster RAG retrieval via Mixedbread.
- **Budget Guard**: Automatically tracks token usage and enforces a hard USD stop.
- **Machine-Readable Local Memory**: Conversations are saved as structured XML blocks in `local_memory.txt`.
- **Traceability**: Captured reasoning chains from models like DeepSeek-R1 are saved to `traceability_audit.txt`.

---

## 🛠️ Setup
1. `pip install openai mixedbread-ai simple-term-menu`.
2. Add API keys to your root: `.nebius_key`, `.mxbai_key`, `.gemini_key`.
3. Update `config.json` with your Mixedbread `store_id`.
