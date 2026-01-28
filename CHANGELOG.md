# Changelog
All notable changes to the Bically AI project will be documented in this file.

## [1.8.5-GOLDEN-ALPHA] - 2026-01-28
### Added
- **Clean-Surface Semantic Indexing**: Implemented regex-based XML stripping in `vectordb.py` to decouple searchable payloads from structural metadata.
- **Ghost Pruning**: Added a 0.65 similarity threshold to filter out background noise from deleted cloud indices.
- **Session Telemetry**: Integrated `SESSION_ID` into system prompts for cold-boot traceability.

### Changed
- **System Prompt Architecture**: Refactored to a role-based `<stream>` reasoning model to improve Kate/User identity recall.
- **Sync Latency**: Reduced `time.sleep` from 2.0s to 0.5s for improved UI thread responsiveness.

### Fixed
- **Vector Dilution**: Resolved issue where XML tags (`<ENTRY>`, `<USER>`) were skewing embedding scores and causing identity amnesia.
- **Graceful Shutdown**: Added exit handlers to `main.py` to prevent hanging terminal sessions.

### TODO / Glitches
- [ ] **Asynchronous I/O**: Move `save_response` to a background thread to eliminate the 500ms blocking lag.
- [ ] **Metadata Filtering**: Explore Mixedbread-side filtering to ignore "Legacy/Unknown" tags before they hit the local threshold.
