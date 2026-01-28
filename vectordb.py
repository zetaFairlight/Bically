import json
import datetime
import uuid
from mixedbread import Mixedbread
from pinecone import Pinecone, ServerlessSpec

# Singleton storage
_mxb_client = None
_pinecone_index = None

def get_clients():
    """Initializes and returns both MXB and Pinecone singletons."""
    global _mxb_client, _pinecone_index
    if _mxb_client and _pinecone_index:
        return _mxb_client, _pinecone_index
    
    with open("config.json", "r") as f:
        config = json.load(f)
    
    mem_cfg = config["memory"]
    
    # 1. Init Mixedbread (The Embedder)
    with open(mem_cfg["mxbai"]["api_key_file"], "r") as f:
        mxb_key = f.read().strip()
    _mxb_client = Mixedbread(api_key=mxb_key)
    
    # 2. Init Pinecone (The Storage)
    p_cfg = mem_cfg["pinecone"]
    with open(p_cfg["api_key_file"], "r") as f:
        pc_key = f.read().strip()
    
    pc = Pinecone(api_key=pc_key)
    
    # Create index if missing (Serverless)
    if p_cfg["index_name"] not in [idx.name for idx in pc.list_indexes()]:
        pc.create_index(
            name=p_cfg["index_name"],
            dimension=p_cfg["dimension"],
            metric=p_cfg["metric"],
            spec=ServerlessSpec(cloud=p_cfg["cloud"], region=p_cfg["region"])
        )
    
    _pinecone_index = pc.Index(p_cfg["index_name"])
    return _mxb_client, _pinecone_index

def search_memories(query, top_k=3):
    """Retrieves context by embedding query via MXB and searching Pinecone."""
    mxb, index = get_clients()
    try:
        # Generate embedding
        res = mxb.embeddings.create(
            model="mixedbread-ai/mxbai-embed-large-v1",
            input=query,
            normalized=True
        )
        query_vector = res.data[0].embedding
        
        # Search Pinecone
        results = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
        return "\n---\n".join([m.metadata['text'] for m in results.matches])
    except Exception as e:
        print(f">> [Search Error] {e}")
        return ""

def save_response(structured_log, metadata_ext=None, mode="remote"):
    """Syncs interaction to Pinecone using MXB vectors."""
    if mode == "local": return
        
    mxb, index = get_clients()
    try:
        # Generate Vector
        res = mxb.embeddings.create(
            model="mixedbread-ai/mxbai-embed-large-v1",
            input=structured_log,
            normalized=True
        )
        vector = res.data[0].embedding
        
        # Metadata Setup
        uid = str(uuid.uuid4())
        meta = {"text": structured_log, "timestamp": str(datetime.datetime.now())}
        if metadata_ext: meta.update(metadata_ext)
        
        # Upsert
        index.upsert(vectors=[{"id": uid, "values": vector, "metadata": meta}])
        print(f">> [Sync] Cloud memory (v1.9.0) updated: {uid}")
    except Exception as e:
        print(f">> [Sync Error] {e}")
