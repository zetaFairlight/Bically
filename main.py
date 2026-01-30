import json
import argparse
import sys
import uuid
import re 
import time 
import threading 
from openai import OpenAI

from vectordb import save_response, search_memories
from menu import select_model_interactive
from startup_check import run_safety_check
from template_engine import load_template 
import accounting 

APP_VERSION = "v1.9.1-alpha"
SESSION_ID = f"SESS-{uuid.uuid4().hex[:8].upper()}"
DEBUG_MODE = False
last_sync_log = "Initial"

def parse_args():
    parser = argparse.ArgumentParser(description="Bically AI - Hybrid RAG")
    parser.add_argument("--check", action="store_true", help="Run initial consistency check")
    parser.add_argument("--trace", action="store_true", help="Enable CoT tracing")
    parser.add_argument("--model", type=str, help="Skip menu and use specific model ID")
    return parser.parse_args()

def background_save(user_input, answer, session_id):
    """Saves to memory silently in a separate thread."""
    global last_sync_log
    if any(x in answer.lower() for x in ["no access", "real-time", "don't know"]):
        last_sync_log = "Sync skipped (Grounding Guard)"
        return

    if len(user_input) > 10:
        try:
            mem_id = save_response(f"U:{user_input}|A:{answer}", metadata_ext={"sid": session_id})
            last_sync_log = f"Success: {mem_id}"
        except Exception as e:
            last_sync_log = f"Failed: {str(e)}"

def main():
    global DEBUG_MODE, last_sync_log
    args = parse_args()

    if args.check:
        print(f"🔍 Running Safety & Consistency Check...")
        run_safety_check()
    else:
        print(f"🚀 Bically {APP_VERSION} initialized (Fast Boot)")

        is_verbose = args.trace

        try:
            with open("config.json", "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            print("❌ CRITICAL: config.json missing.")
            sys.exit(1)
                
        selected_id = select_model_interactive(list(config["providers"].keys()), config, args.model)
        p_cfg = config["providers"][selected_id]
        
        with open(p_cfg["api_key_file"], "r") as f:
            key = f.read().strip()
            client = OpenAI(api_key=key, base_url=p_cfg["base_url"])
            
            chat_history = []
            print("="*40)

            while True:
                prompt_symbol = "\033[93m(🛠️) You\033[0m" if (is_verbose or DEBUG_MODE) else "You"
                user_input = input(f"\n{prompt_symbol}: ").strip()
                
                if not user_input:
                    continue

                if user_input.startswith("!"):
                    cmd = user_input.lower()
                    if cmd == "!debug":
                        DEBUG_MODE = not DEBUG_MODE
                        print(f">> [System] Debug Toggle: {'ON' if DEBUG_MODE else 'OFF'}")
                    elif cmd in ["!exit", "!quit"]:
                        print("Exiting...")
                        break
                    elif cmd == "!status":
                        print(f"Session: {SESSION_ID} | Last Sync: {last_sync_log}")
                    continue 

                req_start = time.time()
                context = search_memories(user_input) if len(user_input) > 20 else ""
                system_payload = load_template(APP_VERSION, SESSION_ID, context)
                system_payload += "\n\n[STRICT_TRUTH_PROTOCOL]\n- Use <THOUGHT> tags for internal logic."

                try:
                    response = client.chat.completions.create(
                        model=p_cfg["model"], 
                        messages=[{"role": "system", "content": system_payload}] + chat_history[-6:] + [{"role": "user", "content": user_input}]
                    )
                    answer = response.choices[0].message.content
                    latency = round(time.time() - req_start, 2)

                    clean = re.sub(r'<THOUGHT>.*?</THOUGHT>', '', answer, flags=re.DOTALL)
                    clean = re.sub(r'<[^>]+>|\*.*?\*|\[.*?\]', '', clean).strip()
                    
                    if is_verbose or DEBUG_MODE:
                        thoughts = re.findall(r'<THOUGHT>(.*?)</THOUGHT>', answer, flags=re.DOTALL)
                        for t in thoughts:
                            print(f"\n\033[90m[Thought]: {t.strip()}\033[0m")
                    
                    print(f"\nAI: \033[92m{clean}\033[0m")
                    
                    if DEBUG_MODE:
                        print(f">> [Metrics] Latency: {latency}s | Sync Status: {last_sync_log}")

                    t = threading.Thread(target=background_save, args=(user_input, answer, SESSION_ID))
                    t.daemon = True 
                    t.start()

                    chat_history.append({"role": "user", "content": user_input})
                    chat_history.append({"role": "assistant", "content": answer})

                except Exception as e:
                    print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()