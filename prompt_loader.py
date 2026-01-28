import os

def load_system_prompt(template_path, context_data, app_version):
    """
    Reads an external XML template and injects dynamic context.
    
    Args:
        template_path (str): Path to the .xml file.
        context_data (str): The retrieved text from Pinecone/Mixedbread.
        app_version (str): Current app version for logging.
    
    Returns:
        str: The fully formatted system prompt ready for the LLM.
    """
    try:
        if not os.path.exists(template_path):
            # Fallback if file is missing (Safety Guardrail)
            return f"<CRITICAL_WARNING>Template not found at {template_path}. using fallback.</CRITICAL_WARNING>"

        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()

        # Inject Data (Simple replacement)
        # We use a default message if context is empty to keep tags valid
        safe_context = context_data if context_data else "No relevant history found for this query."
        
        filled_prompt = template.replace("{{ context }}", safe_context)
        filled_prompt = filled_prompt.replace("{{ version }}", app_version)

        return filled_prompt.strip()

    except Exception as e:
        return f"<SYSTEM_ERROR>Prompt Loader Failed: {e}</SYSTEM_ERROR>"
