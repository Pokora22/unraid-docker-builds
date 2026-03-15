#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="${SCRIPT_DIR}/venv"

# Create venv if it doesn't exist
if [ ! -f "${VENV_DIR}/bin/python" ]; then
    echo "Creating venv..."
    uv venv "${VENV_DIR}" --python python3 --seed
fi

# Activate venv
source "${VENV_DIR}/bin/activate"
export PYTHON="${VENV_DIR}/bin/python"

echo "Using python: $(which python)"

exec python launch.py --listen $COMMANDLINE_ARGS