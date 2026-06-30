# Prompt Engineering Evaluation Framework [[TH]](docs/README.md)



A local, CI-style framework for evaluating LLM output accuracy. Sends prompts to a locally-running Ollama model and scores responses against ground-truth labels — no external APIs required.

<!-- ```
data/*.json  →  main.py  →  Ollama (gemma4:31b-cloud)  →  eval.py  →  score (0.0–1.0)
``` -->
![alt text](<ChatGPT Image Jun 26, 2026, 04_54_44 PM.png>)

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
ollama pull gemma4:31b-cloud
ollama serve
```

The model is ~19 GB. If the download fails mid-way, re-run `ollama pull gemma4:31b-cloud` — Ollama resumes partial downloads.

**Local** — first, copy your Ollama models into the project:

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.ollama\models" .\models
```

Then serve from the local directory:

```powershell
$env:OLLAMA_MODELS = ".\models"
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
ollama run gemma4:31b-cloud
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
winget install --id Git.Git --exact --source winget --silent --disable-interactivity --accept-source-agreements --accept-package-agreements
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

for Workshop's ECC 704: 

```powershell
Set-Alias gbash "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
```

### 2. Clone the repository

Open **PowerShell** or **Git Bash** (search in the Start menu):

Clone the `gemma4-31b-cloud` branch directly:

```powershell
git clone -b gemma4-31b-cloud https://github.com/windx987/workshop-k-eng-2026.git
cd ./workshop-k-eng-2026
```

> **Note:** The `-b gemma4-31b-cloud` flag checks out this specific branch. If you want the default branch instead, omit `-b gemma4-31b-cloud`.

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

## Jump Start

Run this in PowerShell to create a starter `system_prompt.txt`:

```powershell
echo "You are a university department advisor. Analyze the student's description carefully and recommend the most suitable departments. Be empathetic and encouraging in your response. Explain your reasoning clearly before making recommendations." > system_prompt.txt
```

Then open `system_prompt.txt` in VS Code and customize it to improve your score.

## Usage

Run the full evaluation pipeline:

```powershell
gbash script.sh
```

Run a specific mode:

```powershell
gbash script.sh public   # public cases only (P01-P05)
gbash script.sh hidden   # hidden cases only (P06-P10)
gbash script.sh judge    # prompt judge only
```

Run special scenarios only (SP1–SP5):

```powershell
gbash script_special.sh
```

Run a single test case:

```bash
.venv/Scripts/python.exe main.py data/S1.json
```

## Special Scenarios

Five maximum-difficulty cases (SP1–SP5) in `data/` are designed to stress-test advanced models. Each uses a **stated career goal as a trap** — the student genuinely believes they want field X, but the ground truth is the field they would actually thrive in.

| File | Student identity | Trap departments | Ground truth |
|---|---|---|---|
| SP1 | "I want to be a doctor" | Medicine, Nursing, Public Health | Biomedical Engineering, Electrical Engineering, Physics |
| SP2 | Coder with AI curiosity | Software Engineering, Data Science | Computer Science, Information Technology, Philosophy |
| SP3 | "I want to be a journalist" | Journalism, Communications, Mass Media | Political Science, Economics, Sociology |
| SP4 | Competitive swimmer / future coach | Sports Science, Physical Education | Biochemistry, Physiology, Nutrition Science |
| SP5 | Wattpad writer / content creator | Thai Literature, Film and Digital Media | Psychology, Cognitive Science, Behavioral Science |

Run them with:

```powershell
gbash script_special.sh
```

## Prompt Judge

Write your system prompt in `system_prompt.txt`, then run:

```powershell
gbash script.sh judge
```

## Create Your Own Agent

Once you've written your `system_prompt.txt`, you can bake it into a custom Ollama model:

**1. Generate a Modelfile from your system prompt:**

```powershell
$prompt = Get-Content system_prompt.txt -Raw
$rule = "IMPORTANT: Respond ONLY with a valid JSON object. Do NOT include 'thought', 'reasoning', or any extra keys outside the JSON."
"FROM gemma4:31b-cloud`nSYSTEM `"$prompt`n`n$rule`"" | Out-File -Encoding utf8 Modelfile
```

**2. Create the agent:**

```powershell
ollama create my-advisor -f Modelfile
```

**3. Chat with your agent:**

```powershell
ollama run my-advisor
```

**4. Run the evaluation using your agent:**

Change `MODEL` in `main.py` from `"gemma4:31b-cloud"` to `"my-advisor"`, then run:

```powershell
gbash script.sh
```

> **Tip:** Every time you update `system_prompt.txt`, re-run steps 1–2 to rebuild the agent.

<!-- ## Adding Test Cases

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
``` -->

