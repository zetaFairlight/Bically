import os

def clear_logs():
    files_to_clear = ["local_memory.txt", "traceability_audit.txt"]
    
    print("🧹 Cleaning old, unstructured logs...")
    
    for file in files_to_clear:
        if os.path.exists(file):
            try:
                # Open in write mode to truncate the file to 0 bytes
                with open(file, "w") as f:
                    pass
                print(f"✅ Cleared: {file}")
            except Exception as e:
                print(f"❌ Could not clear {file}: {e}")
        else:
            print(f"ℹ️ {file} does not exist. Skipping.")

    print("\n🚀 Log reset complete. Bically is ready for v1.5.5 structured data.")

if __name__ == "__main__":
    clear_logs()
