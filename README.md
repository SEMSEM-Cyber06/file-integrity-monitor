# File Integrity Monitor

A lightweight Python tool that watches a folder and alerts you when a file inside it is modified. It works by computing a SHA-256 hash of every file and comparing the hashes on a regular schedule. If a file's content changes, its hash changes, and the tool flags it.

Built as a hands-on security project to practice file integrity monitoring (FIM), a common defensive technique used to detect tampering.

## Features

- Scans a folder and its subfolders and hashes every file with SHA-256
- Reads files in chunks, so large files don't use much memory
- Re-scans every 10 seconds and compares against the previous scan
- Prints an alert to the console when a file is modified
- Writes alerts and start events to a log file with timestamps
- Saves the latest hashes to a JSON file
- Creates the monitored folder automatically if it doesn't exist

## Requirements

- Python 3.8 or newer (uses the `:=` operator)
- No external libraries, only the Python standard library

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/SEEMSEM-cyber06/file-integrity-monitor.git
   cd file-integrity-monitor
   ```
2. Run the script:
   ```
   python file_monitor.py
   ```
3. On the first run it creates a `monitor_folder` directory. Put the files you want to watch inside it.
4. Edit any file in `monitor_folder` and within about 10 seconds you will see:
   ```
   [ALERT] File modified: monitor_folder/example.txt
   ```
5. Press `Ctrl + C` to stop the monitor.

## Configuration

These settings are at the top of `file_monitor.py`:

| Variable | Default | Purpose |
|---|---|---|
| `MONITOR_PATH` | `monitor_folder` | Folder to watch |
| `HASH_DB` | `hashes.json` | File where hashes are stored |
| `LOG_FILE` | `integrity.log` | File where events are logged |

The scan interval is set by `time.sleep(10)` in the `monitor()` function.

## How it works

1. **Baseline:** on startup, every file in the folder is hashed and saved.
2. **Scan loop:** every 10 seconds the folder is hashed again.
3. **Compare:** each file's new hash is compared with its previous hash.
4. **Alert:** if the hashes differ, the file was modified, so an alert is printed and logged.

## Project structure

```
file-integrity-monitor/
├── file_monitor.py   # main script
├── README.md
├── monitor_folder/   # created on first run
├── hashes.json       # created on first run
└── integrity.log     # created on first run
```

## Limitations and ideas for improvement

This is a learning project, so it is intentionally simple:

- Only **modified** files are reported. Newly created and deleted files are not detected yet.
- The baseline is rebuilt every time the script starts, so changes made while the monitor was not running are missed.
- Files are compared against the previous scan, not a fixed trusted baseline.
- Files that cannot be read (for example because of permissions) are skipped silently.
- Scanning is done by polling every 10 seconds, not by real-time file system events.

Possible next steps: detect added and deleted files, keep a persistent trusted baseline, add email or desktop notifications, and use real-time events with the `watchdog` library.

## Disclaimer

For educational use. It is not a replacement for professional intrusion detection tools such as AIDE, Tripwire, or OSSEC.