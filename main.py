import json
import argparse
import sys
import os
import uuid
from openai import OpenAI
from vectordb import save_response, search_memories
from menu import select_model_interactive

# Unique Session ID for traceability
SESSION_ID = f"SESS-{uuid.uuid4().hex[:8].upper()}"
APP_VERSION = "1.8.5-GOLDEN"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", type=str)
    args = parser.parse_args()

    # Load Config & Select Model
    with open("config.json", "r") as f: config = json.load(f)
    available_models = list(config["providers"].keys())
    args.model = select_model_interactive(available_models, config, args.model)
    
    p_cfg = config["providers"][args.model]
    with open(p_cfg["api_key_file"], "r") as f: api_key = f.read().strip()
    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    chat_history = [] 
    print(f"\n🚀 Bically v{APP_VERSION} | Session: {SESSION_ID}")

    while True:
        user_input = input("\nYou: ").strip()
        if not user_input or user_input.lower() in ["exit", "quit"]: break

        # 1. SEARCH LONG-TERM MEMORY
        # We query the cloud for relevant context before the AI answers
        context = search_memories(user_input)

        # 2. CONSTRUCT PROMPT
        system_content = f"""
<SYSTEM_PROMPT>
  <IDENTITY>You are Bically, a helpful AI assistant with long-term memory.</IDENTITY>
  <KNOWLEDGE_BASE>
    <CLOUD_MEMORIES>
    {context if context else "No relevant long-term memories found."}
    </CLOUD_MEMORIES>
  </KNOWLEDGE_BASE>
  <INSTRUCTIONS>
    - If the user asks about a personal fact (e.g., "favorite color"), CHECK <CLOUD_MEMORIES> FIRST.
    - If the information is in <CLOUD_MEMORIES>, use it to answer.
    - If the info is missing, politely ask for it.
  </INSTRUCTIONS>
</SYSTEM_PROMPT>"""

        messages = [{"role": "system", "content": system_content.strip()}]
        messages.extend(chat_history[-6:]) 
        messages.append({"role": "user", "content": user_input})

        try:
            # Generate Answer
            response = client.chat.completions.create(model=p_cfg["model"], messages=messages)
            answer = response.choices[0].message.content
            print(f"\nAI: {answer}")
            
            # Update Short-term History
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": answer})

            # 3. SAVE TO LONG-TERM MEMORY
            # Structure the data as XML for better semantic retrieval later
            structured_log = f"<ENTRY>\n  <USER>{user_input}</USER>\n  <AI>{answer}</AI>\n</ENTRY>"
            
            save_response(
                structured_log, 
                metadata_ext={"session_id": SESSION_ID},
                mode="local" if args.dry_run else "remote"
            )

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
