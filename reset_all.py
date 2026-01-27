import os
import json
from mixedbread import Mixedbread

def reset_cloud():
    print("☁️ Initializing Cloud Reset...")
    try:
        # 1. Load Configuration
        with open("config.json", "r") as f:
            cfg = json.load(f)["mxbai"]
        with open(cfg["api_key_file"], "r") as f:
            key = f.read().strip()
        
        client = Mixedbread(api_key=key)
        store_id = cfg["store_id"]

        print(f"🔍 Fetching files from store: {store_id}...")
        
        # 2. List all files currently in the store
        # Mixedbread SDK list() returns an iterator for auto-pagination
        files = client.stores.files.list(store_id)
        file_ids = [f.id for f in files]

        if not file_ids:
            print("✅ Cloud store is already empty.")
            return

        print(f"🗑️ Found {len(file_ids)} files. Starting deletion...")
        
        # 3. Delete each file from the store
        for fid in file_ids:
            client.stores.files.delete(store_identifier=store_id, file_identifier=fid)
            print(f"   [-] Deleted: {fid}")

        print("✨ Cloud store successfully wiped.")
    except Exception as e:
        print(f"❌ Cloud Reset Error: {e}")

def reset_local():
    print("\n💻 Initializing Local Reset...")
    files_to_wipe = ["local_memory.txt", "traceability_audit.txt"]
    
    for filename in files_to_wipe:
        if os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("") # Truncate file to 0 bytes
            print(f"✅ Wiped: {filename}")
        else:
            print(f"ℹ️ {filename} does not exist. Skipping.")

if __name__ == "__main__":
    confirm = input("⚠️ WARNING: This will PERMANENTLY delete all cloud and local memories. Continue? (y/n): ")
    if confirm.lower() == 'y':
        reset_cloud()
        reset_local()
        print("\n🚀 System is now a clean slate for v1.5.5!")
    else:
        print("❌ Reset cancelled.")
