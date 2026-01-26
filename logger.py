import datetime

def log_trace(model_name, query, thinking, answer, file_path="traceability_audit.txt"):
    """Appends the full reasoning chain to a permanent audit file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
==================================================
DATE: {timestamp}
MODEL: {model_name}
USER QUERY: {query}
--------------------------------------------------
THINKING PROCESS (CoT):
{thinking if thinking else "N/A (Non-reasoning model)"}
--------------------------------------------------
FINAL ANSWER:
{answer}
==================================================
"""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)
