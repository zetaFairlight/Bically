import json
import argparse
import sys
import os
import uuid
from openai import OpenAI
from vectordb import save_response, search_memories
from menu import select_model_interactive
import accounting  # <--- Integrated budget tracking

# Unique Session ID for traceability
SESSION_ID = f"SESS-{uuid.uuid4().hex[:8].upper()}"
APP_VERSION = "1.8.5-GOLDEN"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", action="store_true", help="Enable traceability logging")
    parser.add_argument("--dry-run", action="store_true", help="Run in local-only mode (no cloud sync)")
    parser.add_argument("--model", type=str, help="Pre-select a model ID")
    args = parser.parse_args()

    # 1. Load Config & Select Model
    try:
        with open("config.json", "r") as f: 
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found.")
        sys.exit(1)
    
    available_models = list(config["providers"].keys())
    selected_model_id = select_model_interactive(available_models, config, args.model)
    
    p_cfg = config["providers"][selected_model_id]
    
    # 2. Initialize LLM Client
    try:
        with open(p_cfg["api_key_file"], "r") as f: 
            api_key = f.read().strip()
    except FileNotFoundError:
        print(f"❌ Error: API key file '{p_cfg['api_key_file']}' not found.")
        sys.exit(1)
    
    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    chat_history = [] 
    print(f"\n🚀 Bically v{APP_VERSION} | Session: {SESSION_ID}")
    print(f"🧠 Memory Mode: {'LOCAL ONLY' if args.dry_run else 'HYBRID (MXB + PINECONE)'}")

    while True:
        user_input = input("\nYou: ").strip()
        
        # Handle Exit Commands
        if not user_input or user_input.lower() in ["exit", "quit"]:
            print("\n👋 Closing session. Memory synced.")
            break

        # Handle Menu Command
        if user_input.lower() == "/menu":
            selected_model_id = select_model_interactive(available_models, config)
            p_cfg = config["providers"][selected_model_id]
            print(f">> Switched to: {selected_model_id}")
            continue

        # 1. RETRIEVE LONG-TERM MEMORIES (RAG)
        context = ""
        if not args.dry_run:
            print("🔍 Searching cloud memory...")
            context = search_memories(user_input, top_k=config.get("search_top_k", 3))

        # 2. CONSTRUCT STRUCTURED XML PROMPT
        system_content = f"""
        <IDENTITY>You are Bically, a high-precision AI assistant.</IDENTITY>
        <KNOWLEDGE_BASE>
        {context if context else "No relevant long-term memories found."}
        </KNOWLEDGE_BASE>
        <CONSTRAINTS>Be concise and factual. Reference memories if applicable.</CONSTRAINTS>
        """

        messages = [{"role": "system", "content": system_content.strip()}]
        messages.extend(chat_history[-6:])  # Keep last 3 turns of short-term context
        messages.append({"role": "user", "content": user_input})

        try:
            # 3. GENERATE RESPONSE
            response = client.chat.completions.create(
                model=p_cfg["model"], 
                messages=messages
            )
            answer = response.choices[0].message.content
            
            # 4. ACCOUNTING & BUDGETING
            usage = response.usage
            cost = accounting.calculate_cost(
                usage.prompt_tokens, 
                usage.completion_tokens, 
                p_cfg["model"], 
                config
            )
            config["budget"]["current_session_spend"] += cost
            
            # Save updated budget state back to config
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)

            print(accounting.get_session_status(
                config["budget"]["current_session_spend"], 
                config["budget"]["max_usd"], 
                p_cfg["model"]
            ))

            print(f"\nAI: {answer}")
            
            # 5. UPDATE SHORT-TERM HISTORY
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": answer})

            # 6. SYNC TO LONG-TERM MEMORY (STRUCTURED XML)
            structured_log = f"<ENTRY>\n  <USER>{user_input}</USER>\n  <AI>{answer}</AI>\n</ENTRY>"
            
            save_response(
                structured_log, 
                metadata_ext={
                    "session_id": SESSION_ID,
                    "model": selected_model_id,
                    "version": APP_VERSION
                },
                mode="local" if args.dry_run else "remote"
            )

            # 7. TRACEABILITY (Optional Reasoning Log)
            if args.trace and hasattr(response.choices[0].message, 'reasoning_content'):
                with open(config["trace_log"], "a") as f:
                    f.write(f"\n[{SESSION_ID}] Reasoning:\n{response.choices[0].message.reasoning_content}\n")

        except Exception as e:
            print(f"❌ Error during inference: {e}")

if __name__ == "__main__":
    main()
