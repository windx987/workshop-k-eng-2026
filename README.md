# Prompt Engineering Evaluation Framework

A local, CI-style framework for evaluating LLM output accuracy. Sends prompts to a locally-running Ollama model and scores responses against ground-truth labels — no external APIs required.

```
data/*.json  →  main.py  →  Ollama (gemma4:12b)  →  eval.py  →  score (0.0–1.0)
```

## Prerequisites

- **Windows 10 / 11**
- **Git for Windows** (includes Git Bash)
- **Ollama**
- **Python 3.12+**

## Local LLM

### Install Ollama

```powershell
irm https://ollama.com/install.ps1 | iex
```

Open a **new** PowerShell window after installation, then verify:

```powershell
ollama --version
```

### Start Ollama and pull the model

**Default** — download from Ollama registry:

```powershell
ollama pull gemma4:12b
ollama serve
```

The model is ~7.6 GB. If the download fails mid-way, re-run `ollama pull gemma4:12b` — Ollama resumes partial downloads.

**Local** — first, copy your Ollama models into the project:

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.ollama\models" .\models
```

Then serve from the local directory:

```powershell
$env:OLLAMA_MODELS = ".\models"
ollama serve
```

Or point to a different models directory:

```powershell
$env:OLLAMA_MODELS = "C:\Users\<you>\models"
ollama serve
```

### Troubleshooting

#### `ollama serve` fails with "bind: Only one usage of each socket address"

Another Ollama instance is already using port 11434. Stop all Ollama processes first:

```powershell
Stop-Process -Name "ollama*" -Force
```

Then retry `ollama serve`.

### Verify the model

Open a new terminal (keep `ollama serve` running) and start a chat:

```powershell
ollama run gemma4:12b
```

```
>>> hello
Hello! How can I help you today? 😊

>>> /bye
```

If the model responds, the local LLM is ready.

## Installation

### 1. Install Git for Windows

Git Bash is required to run `script.sh`.

```powershell
winget install Git.Git --silent --accept-source-agreements --accept-package-agreements
```

Open a **new** PowerShell window after installation, then verify:

```powershell
git --version
```

Set up a `gbash` alias for Git Bash:

```powershell
Set-Alias gbash "C:\Program Files\Git\bin\bash.exe"
gbash --version
```

> **Note:** This alias only lasts for the current terminal session. Run `Set-Alias` again if you open a new PowerShell window.

### 2. Clone the repository

Open **PowerShell** or **Git Bash** (search in the Start menu):

```powershell
git clone https://github.com/windx987/workshop-k-eng-2026.git
cd ./workshop-k-eng-2026
```

### 3. Install Python 3.12 (optional)

Check if Python is already installed:

```powershell
python --version
```

If you see `Python 3.12.x` or newer, skip to step 4. Otherwise, install it:

```powershell
winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
```

Open a **new** PowerShell window after installation, then verify:

```powershell
python --version
```

If `python` is still not found, add these to your user PATH via **Settings → System → Advanced system settings → Environment Variables → Path (User)**:

```
%USERPROFILE%\AppData\Local\Programs\Python\Python312
%USERPROFILE%\AppData\Local\Programs\Python\Python312\Scripts
```

Then open a new terminal and re-check.

### 4. Create the virtual environment and install dependencies

```bash
python -m venv .venv
.venv/Scripts/pip.exe install -r requirements.txt
```

### 5. Verify the setup

```bash
.venv/Scripts/python.exe main.py data/S1.json
```

You should see JSON output with `recommended_departments`. If so, the setup is complete.

## Usage

Run the full evaluation pipeline:

```powershell
gbash script.sh
```

Run a single test case:

```bash
.venv/Scripts/python.exe main.py data/S1.json
```
<!-- 
Evaluate a response:

```bash
.venv/Scripts/python.exe main.py data/S1.json > /tmp/response.json
.venv/Scripts/python.exe eval.py data/S1.json /tmp/response.json
``` -->

## Adding Test Cases

Drop a `.json` file into `data/` — the pipeline picks it up automatically on the next run.

```json
{
  "scenario_id": "S4",
  "student_text": "I enjoy designing user interfaces and prototyping mobile apps.",
  "allowed_departments": ["Computer Science", "UX/UI Design", "Data Science", "Business Administration"],
  "max_suggestions": 2,
  "gt_departments": ["UX/UI Design"]
}
```

See `MANUAL.md` for full details on test case format and scoring.

## Activating the venv (optional)

Only needed if you want to call `python` without the full path:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks this, run once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

