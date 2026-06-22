import sys
import json


def evaluate(case_path: str, response_path: str) -> dict:
    with open(case_path) as f:
        case = json.load(f)
    with open(response_path) as f:
        response = json.load(f)

    gt = set(case["gt_departments"])
    predicted = set(response.get("recommended_departments", []))
    correct = len(gt & predicted)
    total_gt = len(gt)

    return {
        "scenario_id": case["scenario_id"],
        "correct": correct,
        "total_gt": total_gt,
        "score": round(correct / total_gt, 4) if total_gt > 0 else 0.0,
    }


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python eval.py <case.json> <response.json>", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(evaluate(sys.argv[1], sys.argv[2])))
