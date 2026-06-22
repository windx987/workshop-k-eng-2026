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


def run(case_path: str) -> dict:
    with open(case_path) as f:
        case = json.load(f)

    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": build_prompt(case)}],
        format="json",
    )

    result = json.loads(response.message.content)
    result["scenario_id"] = case["scenario_id"]
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <case.json>", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(run(sys.argv[1])))
