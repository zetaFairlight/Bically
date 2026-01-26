import json
import argparse
import sys
import os
from openai import OpenAI
from vectordb import save_response, search_memories
from logger import log_trace
from menu import select_model_interactive

def check_budget(usage, model_id, config):
    """Calculates cost and exits if budget is exceeded."""
    rates = config["pricing"].get(model_id, {"input": 1.0, "output": 2.0})
    in_cost = (usage.prompt_tokens / 1_000_000) * rates["input"]
    out_cost = (usage.completion_tokens / 1_000_000) * rates["output"]
    total = in_cost + out_cost
    config["budget"]["current_session_spend"] += total
    
    current = config["budget"]["current_session_spend"]
    limit = config["budget"]["max_usd"]
    print(f"💰 Session Spend: ${current:.4f} / ${limit:.2f}")

    if current >= limit:
        print("\n🛑 BUDGET LIMIT REACHED.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", type=str)
    args = parser.parse_args()

    with open("config.json", "r") as f: config = json.load(f)
    available_models = list(config["providers"].keys())
    
    # Init Model
    args.model = select_model_interactive(available_models, config, args.model)
    p_cfg = config["providers"][args.model]
    with open(p_cfg["api_key_file"], "r") as f: api_key = f.read().strip()
    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    # --- HYBRID MEMORY BUFFER (v1.5.2) ---
    chat_history = [] 

    print(f"🚀 Bically v1.5.2 | Hybrid RAG Active | Model: {args.model}")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "/menu":
            args.model = select_model_interactive(available_models, config)
            p_cfg = config["providers"][args.model]
            with open(p_cfg["api_key_file"], "r") as f: api_key = f.read().strip()
            client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)
            print(f"✅ Switched to {args.model}. History preserved.")
            continue 

        if not user_input or user_input.lower() in ["exit", "quit"]: break

        # 1. LONG-TERM RETRIEVAL (Cloud DB)
        context = "MOCK CONTEXT" if args.dry_run else search_memories(user_input)

        # 2. HYBRID PAYLOAD CONSTRUCTION
        messages = [{"role": "system", "content": f"Long-term Cloud Memories: {context}"}]
        
        # Add the last 6 messages (3 turns) for short-term recall
        messages.extend(chat_history[-6:]) 
        messages.append({"role": "user", "content": user_input})

        try:
            if args.dry_run:
                answer, thinking = f"DRY RUN: Response to {user_input}", None
            else:
                response = client.chat.completions.create(model=p_cfg["model"], messages=messages)
                check_budget(response.usage, p_cfg["model"], config)
                thinking = getattr(response.choices[0].message, 'reasoning_content', None)
                answer = response.choices[0].message.content

            if thinking and args.trace: print(f"\n[THOUGHTS]: {thinking}")
            print(f"\nAI: {answer}")
            
            # 3. UPDATE SHORT-TERM MEMORY
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": answer})

            # 4. SYNC TO CLOUD & LOCAL
            if args.trace and not args.dry_run: log_trace(args.model, user_input, thinking, answer)
            save_response(f"User: {user_input} | AI: {answer}", mode="local" if args.dry_run else "remote")

        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()
