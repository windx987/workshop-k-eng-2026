#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

PYTHON=".venv/Scripts/python.exe"
DATA_DIR="data"
HIDDEN_DIR="hidden_data"
PROMPT_FILE="system_prompt.txt"
CIPHER_KEY="workshop2026"
SCORES=()

echo "=== LLM Evaluation Run ==="

for case_file in "$DATA_DIR"/*.json; do
    echo ""
    echo "Running: $(basename "$case_file")"

    "$PYTHON" main.py "$case_file" > /tmp/llm_response.json
    eval_result=$("$PYTHON" eval.py "$case_file" /tmp/llm_response.json)
    echo "  $eval_result"

    score=$(echo "$eval_result" | "$PYTHON" -c "import sys,json; print(json.load(sys.stdin)['score'])")
    SCORES+=("$score")
done

for b64_file in "$HIDDEN_DIR"/P{06..10}.b64; do
    name=$(basename "${b64_file%.b64}")
    tmp_case="/tmp/${name}.json"

    "$PYTHON" -c "
import base64, sys
KEY = b'${CIPHER_KEY}'
raw = base64.b64decode(open('${b64_file}').read())
dec = bytes([b ^ KEY[i % len(KEY)] for i, b in enumerate(raw)])
sys.stdout.buffer.write(dec)
" > "$tmp_case"

    echo ""
    echo "Running: $name (hidden)"

    "$PYTHON" main.py "$tmp_case" > /tmp/llm_response.json
    eval_result=$("$PYTHON" eval.py "$tmp_case" /tmp/llm_response.json)
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
final=$("$PYTHON" -c "s=[$scores_csv]; print(round(sum(s), 4))")

echo ""
echo "=== Final Score: $final / $count cases ==="

echo ""
echo "=== Prompt Judge ==="
if [ -f "$PROMPT_FILE" ]; then
    prompt_eval=$("$PYTHON" prompt_judge.py "$PROMPT_FILE")
    echo "$prompt_eval"
    prompt_score=$(echo "$prompt_eval" | "$PYTHON" -c "import sys,json; print(json.load(sys.stdin).get('total_score', 0))")
    echo ">> Prompt Quality Score: $prompt_score / 100"
else
    echo "Warning: $PROMPT_FILE not found. Skipping prompt evaluation."
fi
