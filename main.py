import sys
import json
import ollama

MODEL = "gemma4:12b"


def build_prompt(case: dict) -> str:
    return (
        f"You are a department recommendation system.\n\n"
        f"Student description: {case['student_text']}\n"
        f"Allowed departments: {', '.join(case['allowed_departments'])}\n"
        f"Maximum suggestions: {case['max_suggestions']}\n\n"
        f"Respond ONLY with a JSON object in this exact format, no other text:\n"
        f'{{"scenario_id": "{case["scenario_id"]}", "recommended_departments": ["Name1"]}}\n\n'
        f"Rules:\n"
        f"- Use only department names from the allowed list (exact spelling)\n"
        f"- Return at most {case['max_suggestions']} departments\n"
        f"- Return only departments genuinely relevant to the student"
    )


MAX_RETRIES = 3

def run(case_path: str) -> dict:
    with open(case_path, encoding="utf-8") as f:
        case = json.load(f)

    prompt = build_prompt(case)
    print(f"=== Case: {case['scenario_id']} ===", file=sys.stderr)
    print(f"Model : {MODEL}", file=sys.stderr)
    print(f"Prompt:\n{prompt}", file=sys.stderr)

    for attempt in range(1, MAX_RETRIES + 1):
        if attempt > 1:
            print(f"\n[Retry {attempt}/{MAX_RETRIES}]", file=sys.stderr)
        print("\n=== Response ===", file=sys.stderr)

        chunks = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            stream=True,
        )

        content = ""
        last = None
        for chunk in chunks:
            piece = chunk.message.content
            content += piece
            print(piece, end="", flush=True, file=sys.stderr)
            last = chunk
        print(file=sys.stderr)

        if last:
            prompt_tokens = last.prompt_eval_count or 0
            gen_tokens = last.eval_count or 0
            tok_per_sec = gen_tokens / (last.eval_duration / 1e9) if last.eval_duration else 0
            total_sec = (last.total_duration or 0) / 1e9
            print(f"\n=== Stats ===", file=sys.stderr)
            print(f"Prompt tokens : {prompt_tokens}", file=sys.stderr)
            print(f"Response tokens: {gen_tokens}", file=sys.stderr)
            print(f"Speed          : {tok_per_sec:.1f} tok/s", file=sys.stderr)
            print(f"Total time     : {total_sec:.2f}s", file=sys.stderr)

        try:
            result = json.loads(content)
            result["scenario_id"] = case["scenario_id"]
            return result
        except json.JSONDecodeError as e:
            print(f"\n[Warning] Invalid JSON: {e}", file=sys.stderr)

    raise RuntimeError(f"Model failed to return valid JSON after {MAX_RETRIES} attempts")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <case.json>", file=sys.stderr)
        sys.exit(1)
    result = run(sys.argv[1])
    if not sys.stdout.isatty():
        print(json.dumps(result))
