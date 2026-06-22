#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

PYTHON=".venv/Scripts/python.exe"
DATA_DIR="data"
SCORES=()

echo "=== LLM Evaluation Run ==="

for case_file in "$DATA_DIR"/*.json; do
    echo ""
    echo "Running: $case_file"

    "$PYTHON" main.py "$case_file" > /tmp/llm_response.json
    eval_result=$("$PYTHON" eval.py "$case_file" /tmp/llm_response.json)
    echo "  $eval_result"

    score=$(echo "$eval_result" | "$PYTHON" -c "import sys,json; print(json.load(sys.stdin)['score'])")
    SCORES+=("$score")
done

count=${#SCORES[@]}

if [ "$count" -eq 0 ]; then
    echo "No test cases found in $DATA_DIR/"
    exit 1
fi

scores_csv=$(IFS=,; echo "${SCORES[*]}")
final=$("$PYTHON" -c "s=[$scores_csv]; print(round(sum(s)/len(s), 4))")

echo ""
echo "=== Final Score: $final / 1.0 ($count cases) ==="
