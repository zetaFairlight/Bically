import os
import json
from mixedbread import Mixedbread

def reset_cloud():
    print("☁️ Initializing Cloud Reset...")
    try:
        # 1. Load Configuration
        if not os.path.exists("config.json"):
            print("❌ config.json not found.")
            return

        with open("config.json", "r") as f:
            cfg = json.load(f)["mxbai"]
        with open(cfg["api_key_file"], "r") as f:
            key = f.read().strip()
        
        client = Mixedbread(api_key=key)
        store_id = cfg["store_id"]

        print(f"🔍 Fetching files from store: {store_id}...")
        
        # 2. Handle the SDK pagination / tuple quirk
        response = client.stores.files.list(store_id)
        files = getattr(response, 'data', response)

        # 3. Delete each file
        deleted_count = 0
        for item in files:
            # Handle tuple return vs object return
            file_obj = item[0] if isinstance(item, tuple) else item
            f_id = getattr(file_obj, 'id', None)
            
            if f_id:
                client.stores.files.delete(store_identifier=store_id, file_identifier=f_id)
                print(f"   [-] Deleted: {f_id}")
                deleted_count += 1

        print(f"✨ Cloud store wiped. Deleted {deleted_count} files.")
    except Exception as e:
        print(f"❌ Cloud Reset Error: {e}")

def reset_local():
    print("\n💻 Initializing Local Reset...")
    files_to_wipe = ["local_memory.txt", "traceability_audit.txt"]
    for filename in files_to_wipe:
        if os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("")
            print(f"✅ Wiped: {filename}")

if __name__ == "__main__":
    confirm = input("⚠️ WARNING: This will PERMANENTLY delete all cloud and local memories. Continue? (y/n): ")
    if confirm.lower() == 'y':
        reset_cloud()
        reset_local()
        print("\n🚀 System is now a clean slate for v1.5.5!")
    else:
        print("❌ Reset cancelled.")
