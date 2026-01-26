# 🛡️ Technical Guardrails & Data Flow

## 1. Budgeting Logic
Pricing is mapped in `config.json`.
- **Formula**: `(input_tokens / 1M * rate) + (output_tokens / 1M * rate)`.
- **Safety**: The system performs a `sys.exit(0)` the moment the limit is breached.

## 2. Total Dry Mode (`--dry-run`)
- **Inference**: Mocks a generic response.
- **Memory**: Overrides `memory_mode` to `local` to ensure zero API calls to Mixedbread.
- **Budget**: Spend is recorded as `$0.0000`.

## 3. Mixedbread SDK Alignment
- Requires `client.files.create()` to generate a File ID.
- Requires `client.stores.files.create()` to attach that file to a specific Vector Store.
