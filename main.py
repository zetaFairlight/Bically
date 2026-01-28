import json
import argparse
import sys
import uuid
from openai import OpenAI
from vectordb import save_response, search_memories
from menu import select_model_interactive
from startup_check import run_safety_check 
import accounting 
from prompt_loader import load_system_prompt  # New dynamic loader

# Global Constants
APP_VERSION = "1.9.1-alpha"
SESSION_ID = f"SESS-{uuid.uuid4().hex[:8].upper()}"
PROMPT_TEMPLATE_PATH = "templates/orchestrator.xml" # Path to your external XML

def main():
    # 1. DECOUPLED PRE-FLIGHT CHECK
    run_safety_check()

    # 2. CLI ARGUMENTS
    parser = argparse.ArgumentParser(description=f"Bically AI Orchestrator {APP_VERSION}")
    parser.add_argument("--trace", action="store_true", help="Enable reasoning chain logging")
    parser.add_argument("--dry_run", action="store_true", help="Local-only mode (no API calls)")
    parser.add_argument("--model", type=str, help="Skip menu and use specific model ID")
    args = parser.parse_args()

    # 3. CONFIGURATION & STATE LOADING
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ CRITICAL: config.json missing from root.")
        sys.exit(1)
    
    # 4. INTERACTIVE MODEL SELECTION
    available_models = list(config["providers"].keys())
    selected_id = select_model_interactive(available_models, config, args.model)
    p_cfg = config["providers"][selected_id]
    
    # 5. LLM CLIENT INITIALIZATION
    with open(p_cfg["api_key_file"], "r") as f:
        api_key = f.read().strip()
    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    chat_history = [] 
    print(f"\n🚀 Bically v{APP_VERSION} | Session: {SESSION_ID}")
    print(f"📡 Provider: {selected_id} | Memory: {'LOCAL-ONLY' if args.dry_run else 'HYBRID-PINECONE'}")

    # 6. MAIN CHAT LOOP
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input or user_input.lower() in ["exit", "quit"]:
                break
            
            if user_input.lower() == "/menu":
                selected_id = select_model_interactive(available_models, config)
                p_cfg = config["providers"][selected_id]
                continue

            # A. RAG RETRIEVAL (Pinecone Query via Mixedbread Vector)
            context = ""
            if not args.dry_run:
                print("🔍 Querying Hybrid Memory...")
                context = search_memories(user_input, top_k=config.get("search_top_k", 3))

            # B. DECOUPLED PROMPT ASSEMBLY
            # Fetches the template from /templates and injects the context
            system_content = load_system_prompt(
                PROMPT_TEMPLATE_PATH, 
                context, 
                APP_VERSION
            )

            if args.trace:
                print(f"\n--- [DEBUG: System Prompt] ---\n{system_content}\n---")

            messages = [{"role": "system", "content": system_content}]
            messages.extend(chat_history[-6:]) # Short-term memory window
            messages.append({"role": "user", "content": user_input})

            # C. INFERENCE
            response = client.chat.completions.create(
                model=p_cfg["model"], 
                messages=messages
            )
            answer = response.choices[0].message.content
            
            # D. PERSISTENT ACCOUNTING
            usage = response.usage
            cost = accounting.calculate_cost(usage.prompt_tokens, usage.completion_tokens, p_cfg["model"], config)
            config["budget"]["current_session_spend"] += cost
            
            # Flush session spend to disk immediately
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)

            print(accounting.get_session_status(
                config["budget"]["current_session_spend"], 
                config["budget"]["max_usd"], 
                p_cfg["model"]
            ))
            
            print(f"\nAI: {answer}")
            
            # E. UPDATE HISTORY & SYNC TO PINECONE
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": answer})

            # Save full structured log for future RAG retrieval
            save_response(
                f"<ENTRY><USER>{user_input}</USER><AI>{answer}</AI></ENTRY>", 
                metadata_ext={"session_id": SESSION_ID, "ver": APP_VERSION},
                mode="local" if args.dry_run else "remote"
            )

        except KeyboardInterrupt:
            print("\n👋 Session ended by user.")
            break
        except Exception as e:
            print(f"❌ Application Error: {e}")

if __name__ == "__main__":
    main()
