#!/bin/bash

# bash_launcher.sh
# -----------------
# Linux launcher for Password_Cracker
# Creates a virtual environment, installs dependencies,
# checks for /etc/shadow (if root), runs main.py, and cleans up on error.

# Exit Codes:
#  1 - Python3 not installed and couldn't be installed
#  2 - Virtual environment creation or activation failed
#  3 - Dependency installation failed
#  4 - main.py execution failed

set -e

echo "[*] Checking for Python 3..."

if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 not found. Attempting to install it..."
    sudo apt update && sudo apt install -y python3 python3-pip python3-venv || {
        echo "[ERROR] Python 3 installation failed. Exiting."
        exit 1
    }
fi

echo "[+] Python 3 is available."

echo "[*] Creating virtual environment..."
python3 -m venv env || {
    echo "[ERROR] Failed to create virtual environment."
    exit 2
}

echo "[*] Activating virtual environment..."
source env/bin/activate || {
    echo "[ERROR] Failed to activate virtual environment."
    rm -rf env
    exit 2
}

echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing dependencies from requirements.txt..."
pip install -r requirements.txt || {
    echo "[ERROR] Failed to install dependencies."
    deactivate
    rm -rf env
    exit 3
}

echo "[*] Checking for /etc/shadow access..."
if [ "$(id -u)" -eq 0 ] && [ -f /etc/shadow ]; then
    echo "[+] Running as root. /etc/shadow is accessible."
    echo "    You may use tools like 'unshadow' or 'john' for hash prep."
else
    echo "[!] /etc/shadow not available. Run as root for shadow cracking."
fi

echo "[*] Launching main.py..."
python main.py || {
    echo "[ERROR] main.py failed to execute."
    deactivate
    rm -rf env
    exit 4
}

echo "[+] Execution completed. Deactivating virtual environment."
deactivate
