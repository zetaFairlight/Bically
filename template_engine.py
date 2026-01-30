import os

def load_template(version, session_id, knowledge_base):
    path = "templates/orchestrator.xml"
    
    if not os.path.exists(path):
        return f"Identity: Bically {version}. Session: {session_id}. Context: {knowledge_base}"
    
    with open(path, "r") as f:
        template = f.read()
    
    filled = template.replace("{{version}}", version)
    filled = template.replace("{{session_id}}", session_id)
    filled = filled.replace("{{knowledge_base}}", str(knowledge_base))
    filled = filled.replace("{{user_name}}", "Kiki")
    
    return filled
