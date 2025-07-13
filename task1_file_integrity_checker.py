import hashlib
import os
import json

MONITOR_DIR = "monitor"
HASH_FILE = "file_hashes.json"

def calculate_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        print(f"Error hashing {filepath}: {e}")
        return None

def generate_hashes():
    file_hashes = {}
    for root, _, files in os.walk(MONITOR_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            hash_val = calculate_hash(full_path)
            if hash_val:
                file_hashes[full_path] = hash_val
    return file_hashes

def compare_hashes(old, new):
    print("\n--- FILE INTEGRITY CHECK ---")
    for path in new:
        if path not in old:
            print(f"[NEW FILE] {path}")
        elif new[path] != old[path]:
            print(f"[MODIFIED] {path}")
    for path in old:
        if path not in new:
            print(f"[DELETED] {path}")

if __name__ == "__main__":
    print("🔍 Scanning directory for file changes...")
    old_hashes = {}
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            old_hashes = json.load(f)

    new_hashes = generate_hashes()
    compare_hashes(old_hashes, new_hashes)

    with open(HASH_FILE, "w") as f:
        json.dump(new_hashes, f, indent=4)
