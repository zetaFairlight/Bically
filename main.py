import json
import argparse
import sys
from openai import OpenAI
# Importing our modular project components
from vectordb import save_response, search_memories
from logger import log_trace

def main():
    # --- 1. CLI Argument Parsing ---
    parser = argparse.ArgumentParser(description="AI Cloud Controller with Traceability")
    parser.add_argument("--trace", action="store_true", help="Enable 'Deep Thinking' visibility and audit logging")
    parser.add_argument("--local", action="store_true", help="Force local memory mode (saves to text file)")
    parser.add_argument("--cat", type=str, default="General", help="Set the initial metadata category for saving memories")
    args = parser.parse_args()

    # --- 2. Configuration & Initialization ---
    try:
        with open("config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config.json not found. Please create it based on the README.")
        sys.exit(1)
    
    # Priority: CLI Flag > Config File > Default False/Remote
    trace_enabled = args.trace or config.get("traceability", False)
    memory_mode = "local" if args.local else config.get("memory_mode", "remote")
    current_category = args.cat

    # Setup LLM Client (OpenAI-Compatible Interface)
    p_cfg = config[config["active_provider"]]
    try:
        with open(p_cfg["api_key_file"]) as kf:
            api_key = kf.read().strip()
    except FileNotFoundError:
        print(f"Error: API key file {p_cfg['api_key_file']} missing.")
        sys.exit(1)

    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    print(f"--- System Initialized ---")
    print(f"Model: {p_cfg['model']} | Mode: {memory_mode} | Trace: {trace_enabled}")
    print(f"Type '!cat [Name]' to change category or 'exit' to quit.")

    # --- 3. The Main Interaction Loop ---
    while True:
        user_input = input(f"\n[{current_category}] You: ").strip()
        
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit"]:
            break

        # Check for dynamic category change command
        if user_input.startswith("!cat "):
            new_cat = user_input.split(" ", 1)[1]
            current_category = new_cat
            print(f">> Metadata Category updated to: {current_category}")
            continue

        # Step A: Contextual Retrieval (The RAG process)
        print(">> Retrieving context from memories...")
        context = search_memories(user_input, top_k=config.get("search_top_k", 3))

        # Step B: LLM Generation
        # We inject the retrieved context into the system/user message flow
        try:
            response = client.chat.completions.create(
                model=p_cfg["model"],
                messages=[
                    {"role": "system", "content": f"Use the following context to answer:\n{context}"},
                    {"role": "user", "content": user_input}
                ]
            )

            # Extract specific 'reasoning_content' for Traceability (DeepSeek-R1 only)
            thinking = getattr(response.choices[0].message, 'reasoning_content', None)
            answer = response.choices[0].message.content

            # Display "Thinking" if requested and available
            if thinking and trace_enabled:
                print(f"\n--- THINKING PROCESS ---\n{thinking}\n------------------------")
            
            print(f"\nAI: {answer}")

            # Step C: Audit Logging (The Traceability phase)
            if trace_enabled:
                log_trace(p_cfg["model"], user_input, thinking, answer, config.get("trace_log"))

            # Step D: Memory Storage (The Metadata Stamper phase)
            # We save the AI's answer so it can be 'recalled' in future chats
            save_response(answer, category=current_category, mode=memory_mode)

        except Exception as e:
            print(f"\n[Generation Error] {e}")

if __name__ == "__main__":
    main()
