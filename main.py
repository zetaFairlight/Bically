import json
import argparse
import datetime
import os
import uuid
from openai import OpenAI
from vectordb import save_response, search_memories
from menu import select_model_interactive

SESSION_ID = f"SESS-{uuid.uuid4().hex[:8].upper()}"
APP_VERSION = "1.8.5-GOLDEN"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str)
    args = parser.parse_args()

    with open("config.json", "r") as f: config = json.load(f)
    available_models = list(config["providers"].keys())
    args.model = select_model_interactive(available_models, config, args.model)
    
    p_cfg = config["providers"][args.model]
    with open(p_cfg["api_key_file"], "r") as f: api_key = f.read().strip()
    client = OpenAI(base_url=p_cfg["base_url"], api_key=api_key)

    chat_history = [] 
    print(f"\n🚀 Bically v{APP_VERSION} | Session: {SESSION_ID}")

    while True:
        now_ts = datetime.datetime.now().strftime("%H:%M:%S")
        user_input = input(f"\n[{now_ts}] You: ").strip()
        
        if not user_input or user_input.lower() in ["exit", "quit"]: 
            print(f"\n👋 Session {SESSION_ID} closed gracefully.")
            break

        if user_input.lower() == "!debug":
            print("\n" + "="*40)
            print(f"🧠 [SYSTEM DEBUG] | Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            search_memories("user identity name info kate pablo mozart") 
            print(f"Version: {APP_VERSION}")
            print("="*40 + "\n")
            continue

        # 1. RETRIEVAL
        context = search_memories(user_input)

        # 2. THE GOLDEN PROMPT
        # We use Markdown headers inside XML to give the LLM clear visual anchors
        system_content = f"""
### ROLE
You are Bically, an advanced AI with an integrated long-term memory system. Your goal is to provide a seamless, personalized experience by recalling past interactions.

### CONTEXT
- **Current Time:** {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Session ID:** {SESSION_ID}

### MEMORY_RECALL_STREAM
<stream>
{context if context else "No relevant memories found for this query."}
</stream>

### OPERATING_INSTRUCTIONS
1. **Analyze the Stream:** Examine the <stream> for user names, preferences, and facts.
2. **Chronology:** Treat the <ENTRY> with the most recent 'timestamp' as the current truth.
3. **Identity:** If the user's name is in the stream, use it. Do not claim ignorance if the name is present.
4. **Tone:** Be helpful and grounded. If you recall a fact (e.g., "I remember you mentioned Mozart"), mention it naturally.
"""

        messages = [{"role": "system", "content": system_content.strip()}]
        messages.extend(chat_history[-6:]) 
        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat.completions.create(model=p_cfg["model"], messages=messages)
            answer = response.choices[0].message.content
            print(f"\nAI: {answer}")
            
            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": answer})

            # 3. STRUCTURED STORAGE
            # We keep the XML strict for the "Past Conversations Log"
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            structured_log = f"<ENTRY timestamp='{timestamp}'>\n  <USER>{user_input}</USER>\n  <AI>{answer}</AI>\n</ENTRY>"
            
            save_response(structured_log, metadata_ext={"session_id": SESSION_ID})

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
