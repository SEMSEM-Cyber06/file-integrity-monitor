import os  # For file and directory operations
import hashlib # For hashing files
import json # For storing and loading hashes
import time # For sleep and timestamps
import logging # For logging events

MONITOR_PATH = "monitor_folder"  # Directory to monitor
HASH_DB = "hashes.json" # File to store hashes
LOG_FILE = "integrity.log" # Log file for integrity monitoring

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s") # Logging configuration

def get_file_hash(filepath): # Function to compute SHA256 hash of a file
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f: # Read file in binary mode
        while chunk := f.read(4096): # Read file in chunks to handle large files
            sha256.update(chunk) 
    return sha256.hexdigest()

def scan_directory(path): # Function to scan directory and get hashes of all files
    file_hashes = {}
    for root, _, files in os.walk(path): # Walk through directory
        for file in files:
            full_path = os.path.join(root, file) # Get full file path
            try:
                file_hashes[full_path] = get_file_hash(full_path) # Compute and store hash 
            except:
                pass
    return file_hashes

def save_hashes(hashes): # Function to save hashes to a JSON file
    with open(HASH_DB, "w") as f:
        json.dump(hashes, f, indent=4)

def load_hashes(): # Function to load hashes from a JSON file
    if not os.path.exists(HASH_DB):
        return {}
    with open(HASH_DB, "r") as f:
        return json.load(f)

def monitor(): # Main monitoring function
    print("Generating baseline hashes...")
    baseline = scan_directory(MONITOR_PATH) # Initial scan to create baseline
    save_hashes(baseline) # Save baseline hashes

    print("Monitoring started...\n")
    logging.info("File Integrity Monitoring Started") # Log monitoring start

    while True: 
        time.sleep(10) # Wait for 10 seconds before next scan
        current = scan_directory(MONITOR_PATH) # Scan directory again

        for file, new_hash in current.items(): # Compare current hashes with baseline
            old_hash = baseline.get(file) # Get old hash from baseline

            if old_hash and new_hash != old_hash: # If hash has changed or file is new
                alert = f"[ALERT] File modified: {file}" # Alert message
                print(alert)
                logging.warning(alert) # save alert to log

        baseline = current
        save_hashes(baseline) # Update baseline with current hashes

if __name__ == "__main__":
    if not os.path.exists(MONITOR_PATH): # Create monitoring directory if it doesn't exist
        os.makedirs(MONITOR_PATH)  # Create the directory
        print(f"Created folder: {MONITOR_PATH}") 
    monitor()