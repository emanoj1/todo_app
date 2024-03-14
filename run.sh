#!/bin/bash

# Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed"
else
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
    echo ".venv - virtual environment present"
    source .venv/bin/activate
else
    python3 -m venv .venv
    echo ".venv - virtual environment created"
    source .venv/bin/activate
fi

# Install dependencies
pip3 install -r requirements.txt

# Run the main.py script
python3 main.py
