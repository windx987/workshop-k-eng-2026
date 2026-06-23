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

```bash
ollama serve &
ollama pull gemma4:12b
```

The model is ~7.6 GB. If the download fails mid-way, re-run `ollama pull gemma4:12b` — Ollama resumes partial downloads.

**Local** — use a pre-downloaded models directory:

```bash
ollama serve --models /path/to/your/models &
```

Or set the model directory permanently via environment variable before starting:

```powershell
$env:OLLAMA_MODELS = "C:\Users\<you>\models"
ollama serve
```

## Installation

### 1. Install Git for Windows

Git Bash is required to run `script.sh`.

```powershell
winget install Git.Git --silent --accept-source-agreements --accept-package-agreements
```

Open a **new** PowerShell window after installation, then verify:

```powershell
git --version
& "C:\Program Files\Git\bin\bash.exe" --version
```

### 2. Clone the repository

Open **Git Bash** (search "Git Bash" in the Start menu):

```bash
cd /c/Users/$USER/Developer
git clone git@github.com:windx987/workshop-k-eng-2026.git
cd workshop-k-eng-2026
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
C:\Users\<you>\AppData\Local\Programs\Python\Python312
C:\Users\<you>\AppData\Local\Programs\Python\Python312\Scripts
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

```bash
bash script.sh
```

Run a single test case:

```bash
.venv/Scripts/python.exe main.py data/S1.json
```

Evaluate a response:

```bash
.venv/Scripts/python.exe main.py data/S1.json > /tmp/response.json
.venv/Scripts/python.exe eval.py data/S1.json /tmp/response.json
```

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

## Troubleshooting

**PowerShell blocks `.venv\Scripts\Activate.ps1`**
Run this once to allow local scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
