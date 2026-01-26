# 🛡️ Technical Guardrails & Data Flow

## 1. Budgeting Logic
Pricing is mapped in `config.json` for every provider.
- **Formula**: `(input_tokens / 1M * rate) + (output_tokens / 1M * rate)`.
- **Safety**: The system performs a `sys.exit(0)` the moment the limit is breached.

## 2. Total Dry Mode (`--dry-run`)
- **Inference**: Mocks a generic response to avoid API costs.
- **Memory**: Overrides `memory_mode` to `local` to ensure zero API calls to Mixedbread.
- **Budget**: Spend is recorded as `$0.0000`.

## 3. Mixedbread SDK Alignment
To prevent sync errors, `vectordb.py` uses a two-step process:
1. **`client.files.create()`**: Generates a unique File ID for the response text.
2. **`client.stores.files.create()`**: Attaches that File ID to the specific `store_id` with metadata.

## 4. Live Model Switching
- **Trigger**: Detected via string comparison (`/menu`) at the start of the input loop.
- **Re-initialization**: The system re-reads the API key and re-instantiates the `OpenAI` client for the new provider.

## 5. Local Git Guardrails
Sensitive files are protected via `.gitignore`:
- **Secrets**: Any file matching `.*_key` is ignored.
- **Environment**: `venv/` and `__pycache__/` are excluded.
- **Temporary Files**: `last_model.json` and local test scripts are not tracked.
