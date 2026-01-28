import json
import sys
import os
from mixedbread import Mixedbread
from pinecone import Pinecone

def run_safety_check():
    print("🛠️  Bically v1.9.1-alpha: Running Pre-Flight Safety Checks...")
    
    # 1. Load Config
    if not os.path.exists("config.json"):
        print("❌ CRITICAL: config.json missing.")
        sys.exit(1)
        
    with open("config.json", "r") as f:
        config = json.load(f)

    # 2. Check Mixedbread (Embedder)
    try:
        mxb_path = config["memory"]["mxbai"]["api_key_file"]
        with open(mxb_path, "r") as f:
            mxb_key = f.read().strip()
        mxb = Mixedbread(api_key=mxb_key)
        # Ping check
        mxb.embeddings.create(model="mixedbread-ai/mxbai-embed-large-v1", input="test")
        print("✅ Mixedbread AI: Connected & Embedding Model Ready.")
    except Exception as e:
        print(f"❌ CRITICAL: Mixedbread Auth Failed: {e}")
        sys.exit(1)

    # 3. Check Pinecone (Storage)
    try:
        p_cfg = config["memory"]["pinecone"]
        with open(p_cfg["api_key_file"], "r") as f:
            pc_key = f.read().strip()
        pc = Pinecone(api_key=pc_key)
        
        if p_cfg["index_name"] not in [idx.name for idx in pc.list_indexes()]:
            print(f"⚠️  Pinecone: Index '{p_cfg['index_name']}' not found. Initializing...")
        else:
            print(f"✅ Pinecone: Cloud Index '{p_cfg['index_name']}' is online.")
    except Exception as e:
        print(f"❌ CRITICAL: Pinecone Auth Failed: {e}")
        sys.exit(1)

    print("🚀 All systems green. Initializing Bically...\n" + "="*40)

if __name__ == "__main__":
    run_safety_check()
