# MANUAL.md

User manual for the Prompt Engineering Evaluation Framework.

---

## Overview

This system evaluates how well a local LLM (Gemma 4 12B via Ollama) recommends university departments based on a student's description. You write test cases, run the pipeline, and get a score from 0.0 to 1.0.

```
data/*.json  →  main.py  →  Ollama (gemma4:12b)  →  eval.py  →  score
```

---

## Starting Ollama

Ollama must be running before executing any script. Run this once per session:

```powershell
Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
```

Verify it is running:

```powershell
ollama list
# Should show: gemma4:12b
```

---

## Running the full pipeline

From the project root in PowerShell:

```powershell
& "C:\Program Files\Git\bin\bash.exe" script.sh
```

Example output:

```
=== LLM Evaluation Run ===

Running: data/S1.json
  {"scenario_id": "S1", "correct": 2, "total_gt": 2, "score": 1.0}

Running: data/S2.json
  {"scenario_id": "S2", "correct": 1, "total_gt": 1, "score": 1.0}

Running: data/S3.json
  {"scenario_id": "S3", "correct": 1, "total_gt": 1, "score": 1.0}

=== Final Score: 1.0 / 1.0 (3 cases) ===
```

The pipeline runs every `.json` file in `data/` alphabetically.

---

## Running a single test case

**Step 1 — Get the LLM response:**

```powershell
.\.venv\Scripts\python.exe main.py data\S1.json
```

Output:

```json
{"scenario_id": "S1", "recommended_departments": ["Computer Science", "Data Science"]}
```

**Step 2 — Evaluate the response:**

Save the output to a file first, then evaluate:

```powershell
.\.venv\Scripts\python.exe main.py data\S1.json > response.json
.\.venv\Scripts\python.exe eval.py data\S1.json response.json
```

Output:

```json
{"scenario_id": "S1", "correct": 2, "total_gt": 2, "score": 1.0}
```

---

## Writing test cases

All test cases live in `data/` as individual `.json` files. The filename can be anything — the pipeline picks up all `*.json` files in that directory.

**Template:**

```json
{
  "scenario_id": "S4",
  "student_text": "Write the student's description here. Can be messy or informal.",
  "allowed_departments": [
    "Computer Science",
    "UX/UI Design",
    "Data Science",
    "Business Administration"
  ],
  "max_suggestions": 2,
  "gt_departments": [
    "Computer Science"
  ]
}
```

| Field | Type | Description |
|---|---|---|
| `scenario_id` | string | Unique identifier for this case |
| `student_text` | string | The student's free-form description |
| `allowed_departments` | string[] | The full list of departments the model may choose from |
| `max_suggestions` | integer | How many departments the model should return at most |
| `gt_departments` | string[] | Ground truth — the correct answer(s) |

**Rules for `gt_departments`:**
- Department names must match entries in `allowed_departments` exactly (same spelling, same casing)
- Can contain one or more departments
- Scoring is based on how many the model gets right out of this list

**Save the file** as `data/S4.json` (or any name). It will be included automatically on the next run.

---

## Scoring

Each test case is scored independently:

```
score = number of correct predictions / number of ground truth departments
```

Examples:

| Ground truth | Predicted | Score |
|---|---|---|
| CS, Data Science | CS, Data Science | 2/2 = 1.0 |
| CS, Data Science, UX | CS, Data Science | 2/3 = 0.67 |
| CS | Data Science | 0/1 = 0.0 |
| CS | CS, Data Science | 1/1 = 1.0 |

The final score is the average across all test cases.

Scoring is **exact string match** — `"CS"` and `"Computer Science"` are different strings.

---

## Changing the model

The model is set at the top of `main.py`:

```python
MODEL = "gemma4:12b"
```

To switch models, change this value to any model available in `ollama list`. The model must already be pulled — the system does not download models automatically.

---

## File reference

| File | Purpose |
|---|---|
| `main.py` | Sends a test case to Ollama, returns LLM response JSON |
| `eval.py` | Compares LLM response against ground truth, returns score JSON |
| `script.sh` | Runs all cases in `data/`, prints per-case results and final score |
| `data/*.json` | Test cases — add new ones here |
| `requirements.txt` | Python dependencies |
| `.venv/` | Python virtual environment |
