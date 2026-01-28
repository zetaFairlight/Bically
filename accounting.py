import json

def get_session_status(current_spend, max_budget, model_name):
    """Informative only: displays budget status without halting execution."""
    icon = "🔴" if current_spend >= max_budget else "💰"
    return f"[{icon} Internal Budget] Model: {model_name} | Spend: ${current_spend:.4f} / ${max_budget:.2f}"

def calculate_cost(tokens_in, tokens_out, model_name, config):
    """Calculates cost based on config.json pricing table."""
    prices = config.get("pricing", {}).get(model_name, {"input": 0, "output": 0})
    return ((tokens_in * prices["input"]) / 1_000_000) + ((tokens_out * prices["output"]) / 1_000_000)
