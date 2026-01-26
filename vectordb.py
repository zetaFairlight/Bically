import json
import datetime
from mixedbread import Mixedbread

def get_mxb_client():
    """
    Initializes the Mixedbread client using settings from config.json.
    Modular approach: separates API logic from core execution.
    """
    with open("config.json", "r") as f:
        # Load the configuration for the mixedbread provider
        full_cfg = json.load(f)
        cfg = full_cfg["mxbai"]
    
    # Read the API key from its restricted local file
    with open(cfg["api_key_file"], "r") as f:
        key = f.read().strip()
    
    return Mixedbread(api_key=key), cfg["store_id"]

def search_memories(query, top_k=3):
    """
    Retrieves the most relevant context snippets from the Mixedbread Cloud.
    This is the 'Retrieval' phase of our RAG system.
    """
    try:
        client, store_id = get_mxb_client()
        
        # Search indexed content within your specific Cloud Store
        results = client.stores.search(
            query=query,
            store_identifiers=[store_id],
            top_k=top_k
        )
        
        # Extract the text content from the matched results
        context_list = [match.content for match in results.data]
        
        # Join snippets with a separator for better LLM readability
        return "\n---\n".join(context_list)
    
    except Exception as e:
        print(f"[Search Error] Failed to retrieve context: {e}")
        return ""

def save_response(text, category="General", mode="remote"):
    """
    The 'Metadata Stamper'. 
    Saves AI outputs with structural tags (timestamp, version, type).
    This ensures traceability and allows for filtered searches later.
    """
    # 1. Create the structured metadata stamp
    # This is vital for regulatory traceability (Audit Trail)
    stamp = {
        "created_at": datetime.datetime.now().isoformat(),
        "source_type": category,
        "app_version": "1.2.0" # Tracking the version of the logic used
    }

    # 2. Handle Remote (Cloud) Storage
    if mode == "remote":
        client, store_id = get_mxb_client()
        try:
            # We ingest the text as a new file/memory in the store
            # The 'metadata' parameter attaches our stamp to this specific memory
            client.stores.files.create(
                store_id=store_id, 
                content=text,
                metadata=stamp
            )
            print(f">> [Cloud Memory] Success: Stamped as '{category}'.")
        except Exception as e:
            print(f">> [Sync Error] Cloud storage failed: {e}")
            
    # 3. Handle Local (Offline) Fallback
    else:
        log_entry = f"[{stamp['created_at']}] [CAT:{category}] [VER:{stamp['app_version']}]\n{text}\n"
        with open("local_memory.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'-'*20}\n{log_entry}")
        print(">> [Local Memory] Success: Saved to local_memory.txt")
