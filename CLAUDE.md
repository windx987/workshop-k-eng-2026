# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

- **Runtime**: WSL2 (Linux) — Claude Code runs here, but the Python venv and Ollama are Windows-native
- **Python**: `.venv/Scripts/python.exe` (3.12, Windows binary accessible from WSL via `/mnt/c/...`)
- **Ollama**: `gemma4:12b` pre-loaded; server at `localhost:11434`
- **No git repo** — this project is not under version control

## Commands

All commands assume WSL2 shell (bash). Use the Windows Python binary from the venv:

```bash
PYTHON=".venv/Scripts/python.exe"

# Start Ollama (if not running) — from PowerShell or via:
ollama serve &

# Run single test case
$PYTHON main.py data/S1.json

# Evaluate a response
$PYTHON main.py data/S1.json > /tmp/llm_response.json
$PYTHON eval.py data/S1.json /tmp/llm_response.json

# Full pipeline (all cases in data/)
bash script.sh

# Install deps
$PYTHON -m pip install -r requirements.txt
```

## Architecture

A local LLM evaluation framework — treats the LLM as a black-box function and scores outputs against ground-truth labels.

```
data/*.json  →  main.py  →  Ollama (gemma4:12b)  →  eval.py  →  score
```

| File | Role |
|---|---|
| `main.py` | Runner — builds a prompt from a test case, sends it to Ollama, returns JSON with `recommended_departments` |
| `eval.py` | Evaluator — compares predicted vs ground-truth departments, returns per-case score |
| `script.sh` | CI orchestrator — loops over all `data/*.json`, runs main.py + eval.py for each, prints final averaged score |
| `data/*.json` | Test cases — drop new `.json` files here; pipeline picks them up automatically |

## Key Implementation Details

- **Model constant**: `MODEL = "gemma4:12b"` at top of `main.py` — change this to swap models
- **Ollama Python SDK**: `main.py` uses `ollama.chat()` with `format="json"` to force JSON output
- **Scoring**: `|intersection(predicted, ground_truth)| / |ground_truth|` per case, averaged across all cases (0.0–1.0)
- **Exact string match**: "CS" ≠ "Computer Science" — department names must match `allowed_departments` exactly
- **script.sh** uses `.venv/Scripts/python.exe` hardcoded as `PYTHON` and writes temp output to `/tmp/llm_response.json`
