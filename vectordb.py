import json
from mixedbread import Mixedbread

def get_mxb_client():
    with open("config.json", "r") as f:
        cfg = json.load(f)["mxbai"]
    with open(cfg["api_key_file"], "r") as f:
        key = f.read().strip()
    return Mixedbread(api_key=key), cfg["store_id"]

def search_memories(query, top_k=3):
    """Retrieves context from Mixedbread Cloud Store."""
    try:
        client, store_id = get_mxb_client()
        # Search indexed content in your store
        results = client.stores.search(
            query=query,
            store_identifiers=[store_id],
            top_k=top_k
        )
        # Extract text from the matches
        context_list = [match.content for match in results.data]
        return "\n---\n".join(context_list)
    except Exception as e:
        print(f"[Search Error] {e}")
        return ""

def save_response(text):
    """Saves AI output to chosen memory mode."""
    with open("config.json", "r") as f:
        cfg = json.load(f)
    
    if cfg.get("memory_mode") == "remote":
        client, store_id = get_mxb_client()
        try:
            client.stores.files.create(store_id=store_id, content=text)
            print(">> [Cloud Memory] Synced.")
        except Exception as e:
            print(f">> [Sync Error] {e}")
    else:
        with open("local_memory.txt", "a") as f:
            f.write(f"\n{text}\n")
