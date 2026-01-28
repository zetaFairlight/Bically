⚠️ CRITICAL COMPATIBILITY ARCHIVE: v1.8.0-GOLDEN
DO NOT UPGRADE or refactor vectordb.py without verifying these environment-specific constraints. The current environment uses an older mixedbread-ai SDK (v0.x) that is incompatible with v1.x "modern" syntax.

🛑 1. THE TUPLE TRAP (Search Results)
Failure Pattern: Treating search results as Objects (e.g., result.content).

Reality: The SDK returns a List of Tuples.

Enforced Logic: match = item[0] if isinstance(item, tuple) else item.

Consequence: Bypassing this causes AttributeError: 'tuple' object has no attribute 'content'.

🛑 2. THE METHOD DRIFT (Cloud Operations)
Failure Pattern: Using client.index() or client.add().

Reality: These methods do not exist in this venv. Use the Two-Step Creation flow.

Enforced Logic:

client.files.create() (to get file_id).

client.stores.files.create() (to attach to store).

🛑 3. THE 0-BYTE UPLOAD (Byte Streams)
Failure Pattern: Using io.BytesIO, temporary files, or file-like buffers.

Reality: File pointers often fail to reset, resulting in empty cloud files.

Enforced Logic: content_bytes = text.encode("utf-8"). Pass the raw bytes directly to the API.

🛑 4. THE IMPORT ALIAS
Failure Pattern: from mxbai import ...

Reality: The package is installed as mixedbread.

Enforced Logic: Always use from mixedbread import Mixedbread.

🧠 RECOVERY CHECKLIST
If the system crashes after a change:

Check Version: Ensure main.py is at least 1.7.0/1.8.0 logic.

Verify Grep: grep "client.files.create" vectordb.py.

Traceability: If the AI forgets Pablo, the tuple index [0] has likely been removed.
