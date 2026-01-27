import io
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

def search_memories(query, top_k=3):
    client, store_id = get_mxb_client()
    if not client: return ""
    try:
        results = client.stores.search(query=query, store_identifiers=[store_id], top_k=top_k)
        extracted_content = []
        
        for match in results.data:
            # SDK FIX: Check for 'content' directly, fallback to 'input_chunk'
            content = getattr(match, 'content', None) or \
                      (getattr(match.input_chunk, 'content', "") if hasattr(match, 'input_chunk') else "")
            
            if content:
                extracted_content.append(content)
                
        return "\n---\n".join(extracted_content)
    except Exception as e: 
        print(f"⚠️ Memory Search Error: {e}")
        return ""

def save_response(text, category="General", mode="remote"):
    """Saves structured text to Mixedbread and local XML-style log."""
    if mode == "remote":
        client, store_id = get_mxb_client()
        if client and store_id:
            try:
                # Use timestamped filename for cloud uniqueness
                filename = f"mem_{datetime.datetime.now().strftime('%H%M%S')}.txt"
                file_obj = io.BytesIO(text.encode("utf-8"))
                uploaded_file = client.files.create(file=(filename, file_obj))
                client.stores.files.create(
                    store_id, 
                    file_id=uploaded_file.id, 
                    metadata={"source": category, "created_at": str(datetime.datetime.now())}
                )
            except Exception as e: print(f">> [Sync Error] {e}")

    # Local storage uses the new structured XML format
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists("local_memory.txt"):
        with open("local_memory.txt", "w") as f: f.write("")
        
    with open("local_memory.txt", "a", encoding="utf-8") as f:
        f.write(f"\n\n{text}\n")
