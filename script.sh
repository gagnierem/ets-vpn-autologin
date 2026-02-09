
#!/bin/bash

# Set working directory to the script's location
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

source venv/bin/activate

cookie=$(python3 main.py)

if [ -z "$cookie" ] || [ "$cookie" = "" ]; then
    echo "main.py did not return any output or cookie was empty."
    exit 1
fi


# Run openconnect as root with the cookie as the -C argument
sudo openconnect accesvpn.etsmtl.ca -C "$cookie"