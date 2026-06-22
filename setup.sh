#!/usr/bin/env bash
set -euo pipefail

# ── helpers ───────────────────────────────────────────────────────────────────
ok()   { echo "  [OK] $*"; }
fail() { echo ""; echo "  [FAIL] $*"; echo ""; exit 1; }
step() { echo ""; echo "==> $*"; }

# ── steps ─────────────────────────────────────────────────────────────────────
step_find_python() {
    step "Checking Python 3.12+"
    PYTHON=""
    CANDIDATES=("python" "python3")
    for dir in \
        "$HOME/AppData/Local/Programs/Python/"Python3*/  \
        "/c/Program Files/Python3"*/                      \
        "/c/Program Files (x86)/Python3"*/
    do
        if [ -f "${dir}python.exe" ]; then
            CANDIDATES+=("${dir}python.exe")
        fi
    done
    for candidate in "${CANDIDATES[@]}"; do
        if (command -v "$candidate" &>/dev/null || [ -f "$candidate" ]) \
            && "$candidate" --version &>/dev/null 2>&1; then
            ver=$("$candidate" --version 2>&1 | grep -oE '3\.[0-9]+')
            minor=${ver#3.}
            if [ "${minor:-0}" -ge 12 ]; then
                PYTHON="$candidate"
                break
            fi
        fi
    done
    [ -z "$PYTHON" ] && fail "Python 3.12+ not found. Install it first:
       winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements"
    ok "$("$PYTHON" --version)"
}

step_check_ollama() {
    step "Checking Ollama"
    command -v ollama &>/dev/null \
        || fail "Ollama not found. Download from https://ollama.com/download/windows and re-run this script."
    ok "Ollama $(ollama --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
}

step_start_server() {
    step "Starting Ollama server"
    if ollama list &>/dev/null 2>&1; then
        ok "Server already running"
    else
        powershell.exe -Command "Start-Process ollama -ArgumentList serve -WindowStyle Hidden" &>/dev/null
        echo "  Waiting for server to be ready..."
        ready=false
        for i in {1..15}; do
            sleep 1
            if ollama list &>/dev/null 2>&1; then
                ready=true
                break
            fi
        done
        if [ "$ready" = false ]; then
            fail "Ollama server did not respond. Try starting it manually:
       Start-Process \"ollama\" -ArgumentList \"serve\" -WindowStyle Hidden"
        fi
        ok "Server started"
    fi
}

step_check_model() {
    step "Checking model gemma4:12b"
    if ollama list | grep -q "gemma4:12b"; then
        ok "gemma4:12b available"
    else
        echo "  Not found locally — pulling now (~7.6 GB, this may take several minutes)..."
        ollama pull gemma4:12b
        ok "gemma4:12b downloaded"
    fi
}

step_setup_venv() {
    step "Python virtual environment"
    if [ ! -d ".venv" ]; then
        "$PYTHON" -m venv .venv
        ok ".venv created"
    else
        ok ".venv already exists"
    fi
}

step_install_deps() {
    step "Installing Python dependencies"
    .venv/Scripts/pip.exe install -r requirements.txt --quiet
    ok "Packages installed"
}

step_smoke_test() {
    step "Running smoke test"
    result=$(.venv/Scripts/python.exe main.py data/S1.json)
    echo "  $result"
    ok "main.py responded correctly"
}

main() {
    echo "=== Project Setup ==="
    step_find_python
    step_check_ollama
    step_start_server
    step_check_model
    step_setup_venv
    step_install_deps
    step_smoke_test
    echo ""
    echo "┌──────────────────────────────────────────────────┐"
    echo "│  Setup complete.                                 │"
    echo "│                                                  │"
    echo "│  Run the evaluation:                             │"
    echo "│    bash script.sh                                │"
    echo "│                                                  │"
    echo "│  Run a single case:                              │"
    echo "│    .venv/Scripts/python.exe main.py data/S1.json │"
    echo "└──────────────────────────────────────────────────┘"
}

[[ "${BASH_SOURCE[0]}" == "$0" ]] && main
