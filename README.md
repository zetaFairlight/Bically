# 🚀 AI Controller Operations Manual

## 🎮 Execution Commands & Flags
Run the system using the following CLI flags to override `config.json` settings:

| Flag | Description |
| :--- | :--- |
| `--trace` | **Traceability Mode**: Prints the AI's internal "thinking" to the console and logs it to the audit file. |
| `--local` | **Offline Memory**: Bypasses the Mixedbread Cloud and saves/reads from `local_memory.txt`. |

**Example:** `python3 main.py --trace`

---

## 🧠 Currently Integrated Models
These models are pre-configured in your `config.json`:

### 1. DeepSeek-R1 (`nebius_reasoning`)
* **Best For**: Complex logic, coding, and math.
* **Feature**: Provides a "Thinking" process before the answer. Essential for traceability.

### 2. DeepSeek-V3 (`nebius_deepseek`)
* **Best For**: Fast, general-purpose chat and summaries.
* **Feature**: Massive Mixture-of-Experts (MoE) efficiency. High speed, low latency.

### 3. NVIDIA Nemotron-70B (`nebius_nvidia`)
* **Best For**: Natural English flow and "Helpfulness."
* **Feature**: Currently ranks #1 on alignment benchmarks (AlpacaEval) for sounding "human."

---

## 🛠️ Requirements
- `pip install openai mixedbread`
- API Key files in root: `.nebius_key`, `.mxbai_key`, `.gemini_key`.
