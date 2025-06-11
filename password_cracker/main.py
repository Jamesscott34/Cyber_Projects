"""
main.py

Main launcher script for the Password_Cracker project.
Prompts the user for a cracking target (SSH, FTP, ZIP, etc.)
and dispatches the request to the appropriate module.

All output is logged to results/logs.txt, and cracked credentials
are stored in cracked_hashes.txt.

Supported Modules:
- SSH
- FTP
- SMTP
- SQL
- RDP
- ZIP
- TAR
- PDF
- DOCX
- Shadow file (Linux only)

Ensure the following files exist in the root directory:
- passwords.txt
- users.txt
"""

import os
import platform
import importlib
from datetime import datetime

LOG_FILE = "results/logs.txt"

def log_event(message):
    os.makedirs("results", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def get_module_map():
    return {
        "1": ("crack_ssh", "SSH"),
        "2": ("crack_ftp", "FTP"),
        "3": ("crack_smtp", "SMTP"),
        "4": ("crack_sql", "SQL"),
        "5": ("crack_rdp", "RDP"),
        "6": ("crack_zip", "ZIP Archive"),
        "7": ("crack_tar", "TAR Archive"),
        "8": ("crack_pdf", "PDF File"),
        "9": ("crack_docx", "DOCX File"),
        "10": ("crack_shadow", "Linux Shadow Hashes")
    }

def print_menu():
    print("\nSelect a cracking target:")
    for key, (_, name) in get_module_map().items():
        if name == "Linux Shadow Hashes" and platform.system() != "Linux":
            continue
        print(f"{key}. {name}")
    print("0. Exit")

def run_module(module_name):
    try:
        module = importlib.import_module(f"modules.{module_name}")
        if hasattr(module, "main"):
            module.main()
        elif hasattr(module, f"crack_{module_name.split('_')[1]}"):
            getattr(module, f"crack_{module_name.split('_')[1]}")()
        else:
            print(f"[!] No valid entry point found in {module_name}.py")
            log_event(f"[ERROR] No entry point in {module_name}.py")
    except ModuleNotFoundError:
        print(f"[!] Module '{module_name}' not found.")
        log_event(f"[ERROR] Module '{module_name}' not found.")
    except Exception as e:
        print(f"[!] Error running {module_name}: {str(e)}")
        log_event(f"[EXCEPTION] {module_name}: {str(e)}")

def main():
    log_event("===== Program Started =====")
    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            print("Exiting.")
            break
        module_map = get_module_map()
        if choice in module_map:
            mod_name, mod_desc = module_map[choice]
            print(f"[*] Running: {mod_desc}")
            log_event(f"[*] Selected: {mod_desc}")
            run_module(mod_name)
        else:
            print("[!] Invalid selection.")
            log_event("[WARNING] Invalid menu selection.")
    log_event("===== Program Exited =====")

if __name__ == "__main__":
    main()
