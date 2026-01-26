# 🛡️ Technical Guardrails & Data Flow

## 1. Budgeting Logic
Pricing is mapped in `config.json` for every provider.
- **Formula**: `(input_tokens / 1M * rate) + (output_tokens / 1M * rate)`.
- **Safety**: The system performs a `sys.exit(0)` the moment the limit is breached.

## 2. Total Dry Mode (`--dry-run`)
- **Inference**: Mocks a generic response to save LLM costs.
- **Memory**: Overrides `memory_mode` to `local` to ensure zero API calls to Mixedbread.
- **Budget**: Spend is recorded as `$0.0000`.

## 3. Mixedbread SDK Alignment
To prevent sync errors, `vectordb.py` uses a two-step process:
1. **`client.files.create()`**: Generates a unique File ID for the response text.
2. **`client.stores.files.create()`**: Attaches that File ID to your specific `store_id` with metadata stamps.

## 4. Git Guardrails (Local)
Sensitive files are protected via `.gitignore`:
- **Secrets**: Any file matching `.*_key` is ignored.
- **Environment**: `venv/` and `__pycache__/` are excluded.
- **Logs**: Local memory and audit logs are not tracked to keep the repo clean.
