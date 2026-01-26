import json
import os
from simple_term_menu import TerminalMenu

STATE_FILE = "last_model.json"

def get_last_selected():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f).get("last_model")
        except: return None
    return None

def save_last_selected(model_name):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_model": model_name}, f)

def select_model_interactive(available_models, config, pre_select=None):
    last_choice = get_last_selected()
    target_model = pre_select if pre_select in available_models else last_choice
    
    menu_entries = available_models + [" [⚙️ Edit Budget] ", " [🚪 Quit] "]
    
    try:
        start_index = menu_entries.index(target_model)
    except ValueError:
        start_index = 0

    print(f"\n--- Model Selection | Current Budget: ${config['budget']['max_usd']:.2f} ---")
    menu = TerminalMenu(
        menu_entries,
        title="Select an LLM or modify settings:",
        cursor_index=start_index,
        menu_cursor=">> ",
        menu_cursor_style=("fg_cyan", "bold"),
        menu_highlight_style=("bg_cyan", "fg_black")
    )
    
    choice_index = menu.show()
    if choice_index is None: exit()
    selected = menu_entries[choice_index]

    if "Edit Budget" in selected:
        new_val = input(f"Enter new USD limit (Current: {config['budget']['max_usd']}): ")
        try:
            config["budget"]["max_usd"] = float(new_val)
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
        except ValueError:
            print("Invalid input.")
        return select_model_interactive(available_models, config, pre_select)
    
    if "Quit" in selected: exit()

    save_last_selected(selected)
    return selected
