#!/bin/bash

# Exit immediately if any command fails
set -e

VENV_PATH=".venv"
VENV_CREATED=false

# Cleanup function for error handling / rollback
cleanup() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        echo -e "\n\033[31mAn error occurred during setup. Rolling back...\033[0m"
        if [ "$VENV_CREATED" = true ] && [ -d "$VENV_PATH" ]; then
            echo "Removing incomplete virtual environment ($VENV_PATH)..."
            rm -rf "$VENV_PATH"
        fi
        echo -e "\033[31mSetup failed.\033[0m"
    fi
}

# Trap script exit to trigger cleanup on failure
trap cleanup EXIT

echo "Installing Python 3.12.0 via pyenv..."
pyenv install 3.12.0

echo "Setting local Python version to 3.12.0..."
pyenv local 3.12.0

echo "Creating virtual environment..."
if [ ! -d "$VENV_PATH" ]; then
    python -m venv "$VENV_PATH"
    VENV_CREATED=true
fi

echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

echo "Upgrading pip..."
# pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "Installing packages from requirements.txt..."
    pip install -r requirements.txt
else
    echo "Warning: requirements.txt not found. Skipping package installation."
fi

# Clear the trap on successful completion so cleanup doesn't run on normal exit
trap - EXIT
echo -e "\033[32mVirtual environment is ready and packages are installed!\033[0m"