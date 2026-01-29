import os
import json
from pinecone import Pinecone

def reset_cloud():
    print("☁️  Initializing Cloud Reset (Pinecone)...")
    try:
        # 1. Load Configuration
        if not os.path.exists("config.json"):
            print("❌ config.json not found.")
            return

        with open("config.json", "r") as f:
            config = json.load(f)
        
        p_cfg = config["memory"]["pinecone"]
        
        # 2. Initialize Pinecone
        with open(p_cfg["api_key_file"], "r") as f:
            pc_key = f.read().strip()
        
        pc = Pinecone(api_key=pc_key)
        index = pc.Index(p_cfg["index_name"])

        # 3. Wipe all vectors in the index
        # For serverless indexes, we delete by namespace (default is empty string)
        print(f"🔍 Wiping Pinecone Index: {p_cfg['index_name']}...")
        index.delete(delete_all=True)
        
        print("✨ Cloud Vector Store wiped successfully.")
    except Exception as e:
        print(f"❌ Cloud Reset Error: {e}")

def reset_local():
    print("\n💻 Initializing Local Reset...")
    
    # 1. Clear Audit Logs
    files_to_wipe = ["traceability_audit.txt"]
    for filename in files_to_wipe:
        if os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("")
            print(f"✅ Wiped: {filename}")

    # 2. Reset Budget in config.json
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
            
            config["budget"]["current_session_spend"] = 0.0
            
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            print("✅ Session budget reset to $0.00.")
    except Exception as e:
        print(f"❌ Local Config Reset Error: {e}")

if __name__ == "__main__":
    print("⚠️  Bically v1.9.1-alpha | GLOBAL RESET TOOL")
    confirm = input("WARNING: This will PERMANENTLY delete all cloud vectors and reset session accounting. Continue? (y/n): ")
    
    if confirm.lower() == 'y':
        reset_cloud()
        reset_local()
        print("\n🚀 System is now a clean slate for v1.9.1-alpha!")
    else:
        print("❌ Reset cancelled.")
