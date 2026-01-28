import os
import json
from mixedbread import Mixedbread

def clean_system():
    print("🧹 Starting Selective Purge...")

    # 1. Wipe Local
    if os.path.exists("local_memory.txt"):
        os.remove("local_memory.txt")
        print("✅ Local memory file deleted.")

    # 2. Wipe Remote Files
    try:
        with open("config.json", "r") as f:
            cfg = json.load(f)["mxbai"]
        with open(cfg["api_key_file"], "r") as f:
            key = f.read().strip()
        
        client = Mixedbread(api_key=key)
        store_id = cfg["store_id"]

        print(f"📡 Fetching files from store: {store_id}...")
        
        # List files - returns a list of tuples in your environment
        response = client.stores.files.list(store_id)
        files = getattr(response, 'data', response)
        
        if not files:
            print("ℹ️ No remote files found.")
        else:
            for item in files:
                # UNPACK TUPLE: This is the fix
                f_obj = item[0] if isinstance(item, tuple) else item
                
                print(f"🗑️ Deleting file: {f_obj.id}...")
                try:
                    client.files.delete(f_obj.id)
                except Exception as e:
                    print(f"   ⚠️ Could not delete {f_obj.id}: {e}")
            
            print("✅ Purge attempt complete.")

    except Exception as e:
        print(f"⚠️ Remote Purge failed: {e}")

if __name__ == "__main__":
    clean_system()
