import pathlib

# Folders you want to ignore
IGNORE_FOLDERS = {'venv', '.venv', 'env', '.git', '__pycache__', '.idea', '.vscode'}

def generate_file_list(output_name="project_files.txt"):
    current_dir = pathlib.Path(".")
    relevant_files = []

    # Iterate through all files in the current directory and subdirectories
    for path in current_dir.rglob("*"):
        # Skip if any part of the path is in the ignore list
        if any(part in IGNORE_FOLDERS for part in path.parts):
            continue
        
        # Only add actual files to the list
        if path.is_file():
            relevant_files.append(str(path))

    # Sort and save to the file
    relevant_files.sort()
    with open(output_name, "w", encoding="utf-8") as f:
        f.write("\n".join(relevant_files))
    
    print(f"✅ Success! Relevant files saved to {output_name}")

if __name__ == "__main__":
    generate_file_list()
