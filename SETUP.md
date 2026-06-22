# SETUP.md

Development environment reference for this machine.

---

## Environment

| Tool | Version | Location |
|---|---|---|
| Ollama | 0.30.10+ | `ollama` on PATH |
| gemma4:12b | — | `C:\Users\<you>\.ollama\models\` (pre-downloaded) |
| Git + Git Bash | 2.54+ | `C:\Program Files\Git\bin\bash.exe` |
| Python | 3.12+ | `C:\Users\<you>\AppData\Local\Programs\Python\Python312\python.exe` |
| pip packages | see `requirements.txt` | `.venv\Scripts\` |

---

## First-time setup

Run `setup.sh` from Git Bash — it handles venv creation, dependency install, Ollama server start, and a smoke test automatically:

```bash
bash setup.sh
```

For a new machine, see `INSTALLATION.md` for the manual prerequisites (Git, Ollama, Python) before running this.

---

## Daily workflow

```powershell
# 1. Start Ollama (if not already running)
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden

# 2. Run the full evaluation pipeline
& "C:\Program Files\Git\bin\bash.exe" script.sh
```

---

## Running individual components

```powershell
# LLM inference on one test case
.\.venv\Scripts\python.exe main.py data\S1.json

# Evaluate a saved response
.\.venv\Scripts\python.exe eval.py data\S1.json response.json
```

From Git Bash:

```bash
.venv/Scripts/python.exe main.py data/S1.json
bash script.sh
```

---

## Activating the venv (optional)

Only needed if you want to call `python` without the full path:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks this, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Re-running setup after pulling changes

```bash
bash setup.sh
```

`setup.sh` is idempotent — safe to re-run. It skips steps that are already complete (venv exists, model already pulled, server running).
