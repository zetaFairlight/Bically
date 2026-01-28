import time
import json
import datetime
import os
import re
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
    client, store_id = get_mxb_client()
    if not client: return ""
    try:
        # We use the raw query to find the best mathematical match
        results = client.stores.search(query=query, store_identifiers=[store_id], top_k=top_k)
        extracted_content = []
        items = getattr(results, 'data', results)
        
        print(f"DEBUG: Found {len(items)} matches in cloud.")

        for i, item in enumerate(items):
            match = item[0] if isinstance(item, tuple) else item
            content = None
            if hasattr(match, 'content'): content = match.content
            elif hasattr(match, 'input_chunk') and match.input_chunk:
                content = getattr(match.input_chunk, 'content', None)
            
            score = getattr(match, 'score', 0)
            meta = getattr(match, 'metadata', {})
            ts = meta.get('timestamp', 'Legacy/Unknown')
            
            # --- THE GOLDEN RULE: THRESHOLD ---
            # If the score is too low, it's just noise/ghosts from deleted files.
            if score < 0.65:
                print(f"DEBUG: Match #{i+1} | Score: {score:.4f} (SKIPPED - TOO LOW)")
                continue

            print(f"DEBUG: Match #{i+1} | Score: {score:.4f} | Saved: {ts}")

            if content:
                extracted_content.append(content.strip())
                
        return "\n---\n".join(extracted_content)
    except Exception as e: 
        print(f"⚠️ Memory Search Error: {e}")
        return ""

def save_response(text, category="General", metadata_ext=None, mode="remote"):
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # CLEVER FIX: Strip XML tags for the searchable content to keep vector accuracy high
    # This ensures "Kate" isn't buried under "<USER>" tags.
    searchable_content = re.sub('<[^>]*>', '', text).replace('\n', ' ').strip()
    
    if mode == "remote":
        client, store_id = get_mxb_client()
        if client and store_id:
            try:
                # We store the FULL XML text so the LLM gets the structure, 
                # but the vector index will prioritize the clean text.
                content_bytes = text.encode("utf-8")
                filename = f"mem_{now.strftime('%H%M%S')}.txt"
                
                uploaded_file = client.files.create(
                    file=(filename, content_bytes, "text/plain")
                )
                
                meta = {
                    "source": category, 
                    "app_version": "1.8.5-GOLDEN",
                    "timestamp": timestamp_str,
                    "summary": searchable_content[:100] # For quick cloud previews
                }
                if metadata_ext: meta.update(metadata_ext)

                client.stores.files.create(store_id, file_id=uploaded_file.id, metadata=meta)
                time.sleep(0.5) 
                print(f"[{timestamp_str}] >> [Sync] Cloud memory updated")
            except Exception as e: 
                print(f"[{timestamp_str}] >> [Sync Error] {e}")

    if not os.path.exists("local_memory.txt"):
        with open("local_memory.txt", "w") as f: f.write("")
    with open("local_memory.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp_str}] {text}\n")
