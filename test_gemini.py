#!/usr/bin/env python3
import sys
import json
from openai import OpenAI

def load_settings():
    with open("config.json", "r") as f:
        return json.load(f)

def get_key(path):
    with open(path, "r") as f:
        return f.read().strip()

def main():
    config = load_settings()
    
    # Logic to switch: CLI flag takes priority, then config file
    provider = config["active_provider"]
    if "--google" in sys.argv:
        provider = "google"
        sys.argv.remove("--google")
    elif "--nebius" in sys.argv:
        provider = "nebius"
        sys.argv.remove("--nebius")

    # Get specific settings for the chosen provider
    target = config[provider]
    
    client = OpenAI(
        api_key=get_key(target["api_key_file"]),
        base_url=target["base_url"]
    )

    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Status check."

    try:
        print(f"--- Routing to {provider.upper()} ({target['model']}) ---")
        chat = client.chat.completions.create(
            model=target["model"],
            messages=[{"role": "user", "content": user_input}]
        )
        print(f"\n{chat.choices[0].message.content}")
    except Exception as e:
        print(f"\n[Error]: {e}")

if __name__ == "__main__":
    main()
