# 📝 Release Notes | v1.5.2 (Hybrid Memory & Statefulness)
**Date:** 2026-01-26

## 🚀 Key Improvements
### 1. Hybrid Memory Buffer
- **New Logic**: Implemented a `chat_history` list in `main.py` that stores the last 6 message turns.
- **Impact**: Solves "indexing lag." AI has perfect recall of the current conversation without waiting for the Cloud DB to sync.

### 2. Context Injection Trigger
- **Enhanced Payload**: The system "packs" the API suitcase with three layers: System instructions, Cloud Memory results, and the Local Chat History.

### 3. SDK Error Resiliency
- **Bug Fix**: `vectordb.py` now safely handles nested `content` attributes in Mixedbread search results.
