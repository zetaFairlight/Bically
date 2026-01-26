import json
import argparse
from openai import OpenAI
from vectordb import save_response, search_memories
from logger import log_trace

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", action="store_true", help="Force traceability")
    parser.add_argument("--local", action="store_true", help="Force local memory mode")
    args = parser.parse_args()

    with open("config.json") as f:
        config = json.load(f)
    
    # Overrides from CLI
    trace_enabled = args.trace or config.get("traceability", False)
    memory_mode = "local" if args.local else config.get("memory_mode", "remote")
    
    p_cfg = config[config["active_provider"]]
    client = OpenAI(base_url=p_cfg["base_url"], api_key=open(p_cfg["api_key_file"]).read().strip())

    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]: break

        # 1. Memory Search
        print(">> Searching Cloud Store...")
        context = search_memories(query, top_k=config.get("search_top_k", 3))

        # 2. Reasoning Completion
        response = client.chat.completions.create(
            model=p_cfg["model"],
            messages=[{"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}]
        )

        # 3. Handle Reasoning Trace (CoT)
        thinking = getattr(response.choices[0].message, 'reasoning_content', None)
        answer = response.choices[0].message.content

        if thinking and trace_enabled:
            print(f"\n[THOUGHT PROCESS]\n{thinking}\n")
        
        print(f"AI: {answer}")

        # 4. Audit & Save
        if trace_enabled:
            log_trace(p_cfg["model"], query, thinking, answer, config.get("trace_log"))
        
        save_response(answer, mode=memory_mode)

if __name__ == "__main__":
    main()
