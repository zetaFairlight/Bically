import io
import json
import datetime
from mixedbread import Mixedbread

def get_mxb_client():
    try:
        with open("config.json", "r") as f:
            cfg = json.load(f)["mxbai"]
        with open(cfg["api_key_file"], "r") as f:
            key = f.read().strip()
        return Mixedbread(api_key=key), cfg["store_id"]
    except Exception: return None, None

def search_memories(query, top_k=3):
    client, store_id = get_mxb_client()
    if not client: return "MOCK CONTEXT: (Local mode active)"
    try:
        results = client.stores.search(query=query, store_identifiers=[store_id], top_k=top_k)
        return "\n---\n".join([match.content for match in results.data])
    except Exception as e: return f"Search error: {e}"

def save_response(text, category="General", mode="remote"):
    if mode == "remote":
        client, store_id = get_mxb_client()
        if client and store_id:
            try:
                filename = f"mem_{datetime.datetime.now().strftime('%H%M%S')}.txt"
                file_obj = io.BytesIO(text.encode("utf-8"))
                uploaded_file = client.files.create(file=(filename, file_obj))
                client.stores.files.create(store_id, file_id=uploaded_file.id, metadata={"source": category})
            except Exception as e: print(f">> [Sync Error] {e}")

    with open("local_memory.txt", "a", encoding="utf-8") as f:
        f.write(f"\n--- [{datetime.datetime.now()}] [{category}] ---\n{text}\n")
