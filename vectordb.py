import time
import json
import datetime
import os
from mixedbread import Mixedbread

_client = None
_store_id = None

def get_mxb_client(force_refresh=False):
    global _client, _store_id
    if _client and _store_id and not force_refresh:
        return _client, _store_id
    try:
        if not os.path.exists("config.json"): return None, None
        with open("config.json", "r") as f:
            cfg = json.load(f)["mxbai"]
        with open(cfg["api_key_file"], "r") as f:
            key = f.read().strip()
        _client = Mixedbread(api_key=key)
        _store_id = cfg["store_id"]
        return _client, _store_id
    except Exception: return None, None

def search_memories(query, top_k=5):
    """
    Searches the Mixedbread vector store for relevant memories.
    Handles 'tuple' returns and nested content structures robustly.
    """
    client, store_id = get_mxb_client()
    if not client: return ""
    try:
        # Search the store
        results = client.stores.search(query=query, store_identifiers=[store_id], top_k=top_k)
        extracted_content = []
        
        # 1. Handle Pagination/Data wrapper
        items = getattr(results, 'data', results)
        print(f"DEBUG: Found {len(items)} potential matches in cloud.")

        for i, item in enumerate(items):
            # 2. Handle Tuple vs Object return types
            match = item[0] if isinstance(item, tuple) else item
            
            # 3. AGGRESSIVE CONTENT EXTRACTION
            # Check all possible fields where text might be hidden
            content = None
            if hasattr(match, 'content'): 
                content = match.content
            elif hasattr(match, 'text'): 
                content = match.text
            elif hasattr(match, 'input_chunk') and match.input_chunk:
                content = getattr(match.input_chunk, 'content', getattr(match.input_chunk, 'text', None))
            
            # Debugging Output
            score = getattr(match, 'score', 0)
            c_len = len(content) if content else 0
            print(f"DEBUG: Match #{i+1} | Score: {score:.4f} | Length: {c_len}")

            if content and content.strip():
                extracted_content.append(content.strip())
                
        return "\n---\n".join(extracted_content)
    except Exception as e: 
        print(f"⚠️ Memory Search Error: {e}")
        return ""

def save_response(text, category="General", metadata_ext=None, mode="remote"):
    """
    Saves text to the Cloud Store using a robust byte-stream method.
    Avoids io.BytesIO cursors to prevent 0-byte uploads.
    """
    timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if mode == "remote":
        client, store_id = get_mxb_client()
        if client and store_id:
            try:
                # 1. ENCODE CONTENT DIRECTLY
                # This ensures we have the actual bytes, no file pointers to reset
                content_bytes = text.encode("utf-8")
                filename = f"mem_{datetime.datetime.now().strftime('%H%M%S')}.txt"
                
                # 2. UPLOAD FILE
                # Tuple format: (filename, raw_bytes, mime_type)
                # 'text/plain' helps the indexer understand it immediately
                uploaded_file = client.files.create(
                    file=(filename, content_bytes, "text/plain")
                )
                
                # 3. ATTACH TO STORE
                meta = {"source": category, "app_version": "1.8.5-GOLDEN"}
                if metadata_ext: meta.update(metadata_ext)

                client.stores.files.create(
                    store_id, 
                    file_id=uploaded_file.id, 
                    metadata=meta
                )
                
                # 4. PAUSE FOR INDEXING
                # Give the cloud 2 seconds to register the new file before we move on
                time.sleep(2)
                
                print(f">> [Sync] Cloud memory updated: {uploaded_file.id} ({len(content_bytes)} bytes)")
            except Exception as e: 
                print(f">> [Sync Error] {e}")

    # Local Redundancy Log
    if not os.path.exists("local_memory.txt"):
        with open("local_memory.txt", "w") as f: f.write("")
        
    with open("local_memory.txt", "a", encoding="utf-8") as f:
        sess = metadata_ext.get('session_id', 'N/A') if metadata_ext else 'N/A'
        f.write(f"\n\n{text}\n")
