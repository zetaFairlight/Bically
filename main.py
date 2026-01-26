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
        print("\n🛑 BUDGET LIMIT REACHED. Quitting gracefully.")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="AI Cloud Controller")
    parser.add_argument("--trace", action="store_true", help="Enable audit logging")
    parser.add_argument("--dry-run", action="store_true", help="Total Dry Mode (No API costs)")
    parser.add_argument("--model", type=str, help="Pre-select model in menu")
    args = parser.parse_args()

    if not os.path.exists("config.json"):
        print("!! Error: config.json not found.")
        sys.exit(1)

    with open("config.json") as f:
        config = json.load(f)
    
    available_models = list(config.get("providers", {}).keys())
    args.model = select_model_interactive(available_models, config, pre_select=args.model)
    p_cfg = config["providers"][args.model]
    
    # API Key Loading
    try:
        with open(p_cfg["api_key_file"], "r") as f:
            api_key = f.read().strip()
    except FileNotFoundError:
        print(f"!! Error: Key file {p_cfg['api_key_file']} missing.")
        sys.exit(1)

    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)
    trace_enabled = args.trace or config.get("traceability", False)
    print(f"\n🚀 System Online | Model: {args.model} | Limit: ${config['budget']['max_usd']}")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError: break

        if user_input.lower() == "/menu":
            print("\n🔄 Switching models...")
            args.model = select_model_interactive(available_models, config)
            p_cfg = config["providers"][args.model]
            
            try:
                with open(p_cfg["api_key_file"], "r") as f:
                    api_key = f.read().strip()
                client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)
                print(f"🚀 System Updated | Model: {args.model} | Limit: ${config['budget']['max_usd']}")
            except FileNotFoundError:
                print(f"!! Error: Key file {p_cfg['api_key_file']} missing.")
            continue
        
        if not user_input or user_input.lower() in ["exit", "quit"]: break

        context = "MOCK CONTEXT" if args.dry_run else search_memories(user_input)

        thinking = None
        if args.dry_run:
            answer = f"DRY RUN response to '{user_input}'"
        else:
            try:
                response = client.chat.completions.create(
                    model=p_cfg["model"],
                    messages=[
                        {"role": "system", "content": f"Context: {context}"},
                        {"role": "user", "content": user_input}
                    ]
                )
                check_budget(response.usage, p_cfg["model"], config)
                thinking = getattr(response.choices[0].message, 'reasoning_content', None)
                answer = response.choices[0].message.content
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    print(f"\n⚠️  QUOTA EXHAUSTED: {args.model} is unavailable (Rate Limit).")
                    print(">> Try another model or use --dry-run.")
                else:
                    print(f"\n❌ API ERROR: {e}")
                continue

        if thinking and trace_enabled:
            print(f"\n[THOUGHTS]: {thinking}")
        print(f"\nAI: {answer}")

        if trace_enabled and not args.dry_run:
            log_trace(args.model, user_input, thinking, answer, config.get("trace_log"))
        
        save_response(answer, mode="local" if args.dry_run else "remote")

if __name__ == "__main__":
    main()
