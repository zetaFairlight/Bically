import os

def load_system_prompt(template_path, context_data, app_version):
    """
    Reads an external XML template and injects dynamic context.
    """
    try:
        if not os.path.exists(template_path):
            return f"<CRITICAL_WARNING>Template not found at {template_path}. using fallback.</CRITICAL_WARNING>"

        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        # FIX: Don't inject conversational text. Use structural tags or empty string.
        # If context is empty, we inject nothing so the <KNOWLEDGE_BASE> tag remains clean.
        safe_context = context_data if context_data and context_data.strip() else "<NO_RELEVANT_MEMORIES_FOUND/>"
        
        filled_prompt = template.replace("{{ context }}", safe_context)
        filled_prompt = filled_prompt.replace("{{ version }}", app_version)

        return filled_prompt.strip()

    except Exception as e:
        return f"<SYSTEM_ERROR>Prompt Loader Failed: {e}</SYSTEM_ERROR>"
