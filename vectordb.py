import os
import json
import time
import uuid
from mixedbread_ai import MixedbreadAI
from pinecone import Pinecone

# Load config to get key file paths
with open("config.json", "r") as f:
    config = json.load(f)

# Helper to read keys from files as defined in your config
def get_key(path):
    with open(path, "r") as f:
        return f.read().strip()

# Configuration pulled directly from your uploaded config.json
MB_API_KEY = get_key(config["memory"]["mxbai"][".mxbai_key"])
PINECONE_API_KEY = get_key(config["memory"]["pinecone"][".pinecone_key"])
INDEX_NAME = config["memory"]["pinecone"][".pinecone_key"]

def save_response(text, metadata_ext=None, mode="remote"):    """
Saves text to vector DB.
STRICTLY SILENT: This function must not print to terminal
to prevent cursor hijacking in the main UI loop.
"""
if not MB_API_KEY or not PINECONE_API_KEY:
    return "Error: Missing Keys"

    try:
        # Initialize clients locally for thread safety
        mxb = MixedbreadAI(api_key=MB_API_KEY)
        pc = Pinecone(api_key=PINECONE_API_KEY)

        # 1. Generate Embedding
        res = mxb.embeddings.create(
            model="mixedbread-ai/mxbai-embed-large-v1",
            input=[text],
            normalized=True
            )
        embedding = res.data[0].embedding

        # 2. Prepare Metadata (Using the restored time module)
        metadata = {
        "content": text,
        "timestamp": time.time(),
        "version": "v1.9.1-alpha"
        }
        if metadata_ext:
            metadata.update(metadata_ext)

        # 3. Upsert to Pinecone (Using the restored uuid module)
        index = pc.Index(INDEX_NAME)
        vector_id = f"mem_{uuid.uuid4().hex[:12]}"

        index.upsert(vectors=[(vector_id, embedding, metadata)])

        # Return ID for internal tracking in main.py !status or !debug
        return vector_id

    except Exception as e:
        # We raise the error so the background_save in main.py can catch
        # it and update the last_sync_log variable.
        raise RuntimeError(f"Database Sync Error: {str(e)}")

        def search_memories(query, top_k=3):
    """
    Retrieves context silently.
    Used by main.py to pull Hybrid RAG context.
    """
    try:
        mxb = MixedbreadAI(api_key=MB_API_KEY)
        pc = Pinecone(api_key=PINECONE_API_KEY)

        res = mxb.embeddings.create(
            model="mixedbread-ai/mxbai-embed-large-v1",
            input=[query]
            )
        query_vector = res.data[0].embedding

        index = pc.Index(INDEX_NAME)
        results = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
            )

        # Formats the results into a string for the system prompt
        return "\n---\n".join([m['metadata']['content'] for m in results['matches']])
    except Exception:
        # If search fails, we return an empty string to allow the AI
        # to continue without context rather than crashing.
        return ""
