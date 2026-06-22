```markdown
# 🧠 Prompt Engineering Evaluation Framework (Local LLM System)

## 🎯 Project Overview

This project is a **fully local LLM evaluation framework** that tests how well a model can:

- Follow structured instructions
- Extract correct information from messy inputs
- Produce valid JSON outputs
- Recommend correct departments
- Match ground-truth answers reliably

It treats an LLM as a **black-box function under test**, similar to a software system in a CI pipeline.

---

## 💡 Core Concept

We do NOT treat the LLM as a chatbot.

Instead, we treat it as:

```

LLM = function(input) → output

```

And we evaluate it using deterministic scoring:

```

eval.py = unit test engine
script.sh = test runner (CI)
main.py = execution layer

```

---

## 🏗️ System Architecture

### 🔹 1. LLM Layer (Inference Only)

```

localhost:11434 (Ollama / Llama / Gemma / Mistral)

```

Responsibilities:
- Generate responses only
- No evaluation logic
- No scoring
- No memory of correctness

---

### 🔹 2. Runner Layer (`main.py`)

Responsibilities:

- Send structured prompts to LLM
- Receive raw responses
- Normalize output format (JSON parsing)
- Forward results to evaluator

Flow:

```

input → main.py → LLM → raw output → eval.py

```

---

### 🔹 3. Evaluation Layer (`eval.py`)

This is the core of the system.

It performs **ground-truth based evaluation**.

#### 🧪 Evaluation Logic

We compare:

```

predicted_departments vs ground_truth_departments

```

---

### 📊 Scoring Formula

Each question has a maximum score of **1.0**.

```

score = |intersection(pred, GT)| / |GT|

````

Where:

- `pred` = model predicted departments
- `GT` = ground truth departments

---

### 📌 Example

#### Ground Truth

```json
{
  "gt_departments": [
    "Computer Science",
    "Data Science",
    "UX/UI Design"
  ]
}
````

#### Model Output

```json
{
  "recommended_departments": [
    "Computer Science",
    "Data Science"
  ]
}
```

#### Score

```
correct = 2
gt_size = 3

score = 2 / 3 = 0.67
```

---

### 🔹 4. Automation Layer (`script.sh`)

Responsibilities:

* Run multiple test cases
* Execute `main.py` for each case
* Call `eval.py`
* Aggregate final score

Acts as a **mini CI system for LLM evaluation**

---

## 🔁 Full Pipeline Flow

```
[Test Dataset]
        ↓
   script.sh
        ↓
    main.py
        ↓
   LLM (Ollama)
        ↓
   raw response
        ↓
    eval.py
        ↓
 score computation
        ↓
 final report
```

---

## 📥 Input / Output Format

### 🔸 Input (Test Case)

```json
{
  "scenario_id": "S1",
  "student_text": "messy natural language input...",
  "allowed_departments": [
    "Computer Science",
    "UX/UI Design",
    "Data Science"
  ],
  "max_suggestions": 2,
  "gt_departments": [
    "Computer Science",
    "Data Science"
  ]
}
```

---

### 🔸 Output (LLM Response)

```json
{
  "scenario_id": "S1",
  "recommended_departments": [
    "Computer Science",
    "Data Science"
  ]
}
```

---

### 🔸 Evaluation Output

```json
{
  "scenario_id": "S1",
  "correct": 2,
  "total_gt": 3,
  "score": 0.67
}
```

---

## 📊 Final Dataset Score

For N test cases:

```
final_score = (Σ individual_scores) / N
```

Each test case contributes equally:

* Max = 1.0
* Min = 0.0

---

## 🧱 Why This Design is Strong

✔ Fully local
No external APIs required

✔ Deterministic evaluation
Same input → same output score

✔ Simple scoring model
Easy to understand and debug

✔ CI-style architecture
Works like software testing pipelines

✔ Scalable
Supports:

* new models
* new datasets
* regression testing
* benchmarking

---

## 🧠 Mental Model

```
main.py   → function under test
LLM       → black-box system
eval.py   → unit test assertions
script.sh → CI test runner
```

---

## 🚀 Future Extensions

### 📈 Benchmarking

* Compare multiple models (Llama vs Gemma vs Mistral)
* Track score improvements over time

---

### 🗃️ Dataset Expansion

* More messy student inputs
* Edge cases
* Ambiguous queries

---

### 📊 Leaderboard System

* Store results in SQLite
* Rank models by score

---

### 🧪 Advanced Evaluation

* Top-K accuracy
* Weighted departments
* Synonym matching (CS ≈ Computer Science)

---

## 🔥 Summary

This project is:

> A local, CI-style evaluation framework for testing LLM behavior using deterministic ground-truth scoring.

It transforms prompt engineering into a measurable, repeatable engineering discipline.

```
```
