import json
import argparse
import sys
import os
from openai import OpenAI
from vectordb import save_response, search_memories
from logger import log_trace
from menu import select_model_interactive

def check_budget(usage, model_id, config):
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
    args.model = select_model_interactive(available_models, config, args.model)
    p_cfg = config["providers"][args.model]
    with open(p_cfg["api_key_file"], "r") as f: api_key = f.read().strip()
    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    chat_history = [] 

    print(f"🚀 Bically v1.5.5 | Structured XML Hybrid Active | Model: {args.model}")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "/menu":
            args.model = select_model_interactive(available_models, config)
            p_cfg = config["providers"][args.model]
            with open(p_cfg["api_key_file"], "r") as f: api_key = f.read().strip()
            client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)
            print(f"✅ Switched to {args.model}.")
            continue 
        if not user_input or user_input.lower() in ["exit", "quit"]: break

        # 1. RETRIEVE LONG-TERM CONTEXT
        context = "MOCK CONTEXT" if args.dry_run else search_memories(user_input)

        # 2. STRUCTURED XML PAYLOAD CONSTRUCTION
        # This adheres to the Anthropic-style structural standard
        system_content = f"""
<SYSTEM_PROMPT>
  <IDENTITY>
    You are Bically, a stateful AI collaborator.
  </IDENTITY>
  <KNOWLEDGE_BASE>
    <CLOUD_MEMORIES>
    {context if context else "No relevant long-term memories found."}
    </CLOUD_MEMORIES>
  </KNOWLEDGE_BASE>
  <CONSTRAINTS>
    - Use the KNOWLEDGE_BASE to recognize the user and past facts.
    - Be concise, helpful, and never mention being an AI.
  </CONSTRAINTS>
</SYSTEM_PROMPT>
"""
        messages = [{"role": "system", "content": system_content.strip()}]
        messages.extend(chat_history[-6:]) 
        messages.append({"role": "user", "content": user_input})

        try:
            if args.dry_run:
                answer, thinking = f"DRY RUN: Structured Response to {user_input}", None
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

            # 4. SYNC TO CLOUD & LOCAL (XML Formatted)
            if args.trace and not args.dry_run: log_trace(args.model, user_input, thinking, answer)
            
            # Formatting the saved entry as XML for better future parsing
            structured_log = f"""
<ENTRY>
  <USER>{user_input}</USER>
  <AI>{answer}</AI>
</ENTRY>"""
            save_response(structured_log.strip(), mode="local" if args.dry_run else "remote")

        except Exception as e:
            print(f"❌ Error: {e}")
            continue

if __name__ == "__main__":
    main()
