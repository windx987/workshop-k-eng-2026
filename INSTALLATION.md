# INSTALLATION.md

Installation guide for the Prompt Engineering Evaluation Framework.

**Platform:** Windows 10 / 11 · PowerShell + Git Bash

---

## What setup.sh does automatically

Once the three prerequisites below are installed, `setup.sh` handles everything else:

- Starts the Ollama server
- Pulls `gemma4:12b` if it is not already on the machine
- Creates the Python virtual environment (`.venv/`)
- Installs all Python dependencies from `requirements.txt`
- Runs a smoke test to confirm the pipeline works

---

## Step 1 — Install Git for Windows

Git Bash is required to run `setup.sh` and `script.sh`.

```powershell
winget install Git.Git --silent --accept-source-agreements --accept-package-agreements
```

Open a **new** PowerShell window after installation, then verify:

```powershell
git --version
& "C:\Program Files\Git\bin\bash.exe" --version
```

---

## Step 2 — Install Ollama

Download the Windows installer from https://ollama.com/download/windows and run it.

Verify in PowerShell:

```powershell
ollama --version
```

---

## Step 3 — Install Python 3.12

```powershell
winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
```

Open a **new** PowerShell window after this completes, then verify:

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

---

## Step 4 — Run setup.sh

Open **Git Bash** (search "Git Bash" in the Start menu), navigate to the project folder, and run:

```bash
cd /c/Users/<you>/Developer/k-eng-workshop-2026
bash setup.sh
```

Or from PowerShell:

```powershell
& "C:\Program Files\Git\bin\bash.exe" -c "cd 'C:\Users\<you>\Developer\k-eng-workshop-2026' && bash setup.sh"
```

`setup.sh` will print its progress at each stage. A successful run ends with:

```
==> Running smoke test
  {"scenario_id": "S1", "recommended_departments": [...]}
  [OK] main.py responded correctly

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

---

## Troubleshooting

**`[FAIL] Python not found`**
Python is not on PATH. Complete Step 3 and open a new terminal before re-running.

**`[FAIL] Ollama not found`**
Complete Step 2 then re-run `setup.sh`.

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

---

## After installation

See `MANUAL.md` for how to write test cases and run evaluations.
