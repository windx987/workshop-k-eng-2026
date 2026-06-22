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

## Installation

### 1. Install Git for Windows

Git Bash is required to run `setup.sh` and `script.sh`.

```powershell
winget install Git.Git --silent --accept-source-agreements --accept-package-agreements
```

Open a **new** PowerShell window after installation, then verify:

```powershell
git --version
& "C:\Program Files\Git\bin\bash.exe" --version
```

### 2. Install Ollama

```powershell
irm https://ollama.com/install.ps1 | iex
```

Open a **new** PowerShell window after installation, then verify:

```powershell
ollama --version
```

### 3. Install Python 3.12

```powershell
winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
```

Open a **new** PowerShell window after installation, then verify:

```powershell
python --version
# Expected: Python 3.12.x
```

If `python` is not found, add these to your user PATH via **Settings → System → Advanced system settings → Environment Variables → Path (User)**:

```
C:\Users\<you>\AppData\Local\Programs\Python\Python312
C:\Users\<you>\AppData\Local\Programs\Python\Python312\Scripts
```

Then open a new terminal and re-check.

### 4. Clone and set up

Open **Git Bash** (search "Git Bash" in the Start menu):

```bash
cd /c/Users/$USER/Developer
git clone git@github.com:windx987/workshop-k-eng-2026.git
cd workshop-k-eng-2026
bash setup.sh
```

Or from PowerShell:

```powershell
& "C:\Program Files\Git\bin\bash.exe" -c "cd 'C:\Users\<you>\Developer\workshop-k-eng-2026' && bash setup.sh"
```

`setup.sh` will automatically:
- Start the Ollama server
- Pull `gemma4:12b` (~7.6 GB) if not already downloaded
- Create a Python virtual environment (`.venv/`)
- Install all Python dependencies from `requirements.txt`
- Run a smoke test to confirm the pipeline works

A successful run ends with:

```
┌──────────────────────────────────────────────────┐
│  Setup complete.                                 │
│                                                  │
│  Run the evaluation:                             │
│    bash script.sh                                │
│                                                  │
│  Run a single case:                              │
│    .venv/Scripts/python.exe main.py data/S1.json │
└──────────────────────────────────────────────────┘
```

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

**`[FAIL] Python not found`**
Python is not on PATH. Complete step 3 and open a new terminal before re-running.

**`[FAIL] Ollama not found`**
Complete step 2 then re-run `setup.sh`.

**`[FAIL] Ollama server did not respond`**
Start Ollama manually in PowerShell, then re-run the script:
```powershell
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
```

**`gemma4:12b` pull takes too long or fails**
The model is 7.6 GB. If the download fails mid-way, re-running `bash setup.sh` resumes it — Ollama caches partial downloads.

**PowerShell blocks `.venv\Scripts\Activate.ps1`**
Run this once to allow local scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
