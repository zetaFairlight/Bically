import json
import argparse
import sys
from openai import OpenAI
from vectordb import save_response, search_memories
from logger import log_trace

def main():
    # --- 1. CLI Argument Parsing ---
    parser = argparse.ArgumentParser(description="AI Cloud Controller")
    parser.add_argument("--trace", action="store_true", help="Enable audit logging")
    parser.add_argument("--local", action="store_true", help="Force local memory mode")
    parser.add_argument("--cat", type=str, default="General", help="Starting category")
    # NEW FLAG: Dry run mode to save tokens
    parser.add_argument("--dry-run", action="store_true", help="Skip API calls and use mock data")
    args = parser.parse_args()

    # --- 2. Configuration & Initialization ---
    with open("config.json") as f:
        config = json.load(f)
    
    trace_enabled = args.trace or config.get("traceability", False)
    memory_mode = "local" if args.local else config.get("memory_mode", "remote")
    current_category = args.cat

    p_cfg = config[config["active_provider"]]
    
    # We only initialize the real client if we aren't in dry-run mode
    client = None
    if not args.dry_run:
        with open(p_cfg["api_key_file"]) as kf:
            api_key = kf.read().strip()
        client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    print(f"--- System Initialized (Dry Run: {args.dry_run}) ---")

    while True:
        user_input = input(f"\n[{current_category}] You: ").strip()
        if not user_input or user_input.lower() in ["exit", "quit"]: break

        if user_input.startswith("!cat "):
            current_category = user_input.split(" ", 1)[1]
            print(f">> Category updated to: {current_category}")
            continue

        # Step A: Memory Search (STILL RUNS in dry-run to test retrieval)
        print(">> Searching memories...")
        context = search_memories(user_input, top_k=config.get("search_top_k", 3))

        # Step B: Inference (Logic Fork)
        if args.dry_run:
            # Simulated Data (No cost)
            thinking = f"DRY RUN: I found context length {len(context)} and I'm analyzing it..."
            answer = f"DRY RUN: This is a mock response to: '{user_input}'"
        else:
            # Real LLM Call (Costs tokens)
            response = client.chat.completions.create(
                model=p_cfg["model"],
                messages=[
                    {"role": "system", "content": f"Context:\n{context}"},
                    {"role": "user", "content": user_input}
                ]
            )
            thinking = getattr(response.choices[0].message, 'reasoning_content', None)
            answer = response.choices[0].message.content

        # Step C: Output & Audit
        if thinking and trace_enabled:
            print(f"\n[THOUGHTS]: {thinking}")
        
        print(f"\nAI: {answer}")

        if trace_enabled:
            log_trace(p_cfg["model"], user_input, thinking, answer, config.get("trace_log"))
        
        save_response(answer, category=current_category, mode=memory_mode)

if __name__ == "__main__":
    main()
