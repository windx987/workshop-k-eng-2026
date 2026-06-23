import sys
import json
import os
import ollama

MODEL = "gemma4:12b"

def build_prompt(case: dict, system_prompt: str) -> str:
    # นำ System Prompt ของนักศึกษามาเป็นหัวใจหลัก แล้วแนบข้อมูลของลีโอแต่ละเคสต่อท้าย
    return (
        f"{system_prompt}\n\n"
        f"=============================\n"
        f"DATA FOR THIS CASE:\n"
        f"Student description: {case['student_text']}\n"
        f"Allowed departments: {', '.join(case['allowed_departments'])}\n"
        f"Maximum suggestions: {case['max_suggestions']}\n"
        f"=============================\n\n"
        f"CRITICAL INSTRUCTION: You MUST respond ONLY with a valid JSON object. "
        f"Place your full coaching conversation, framework analysis, and empathy inside the 'raw_output' field so it can be evaluated.\n\n"
        f"Use this exact format:\n"
        f"{{\n"
        f'  "scenario_id": "{case["scenario_id"]}",\n'
        f'  "raw_output": "Write your full reply to the student here (must include your empathy, analysis, and tone).",\n'
        f'  "recommended_departments": ["Name1", "Name2"]\n'
        f"}}\n\n"
        f"Rules for JSON:\n"
        f"- Use only department names from the allowed list (exact spelling)\n"
        f"- Return at most {case['max_suggestions']} departments"
    )

def run(case_path: str) -> dict:
    # 1. โหลดข้อมูลเคสทดสอบ (รองรับภาษาไทยด้วย utf-8)
    with open(case_path, encoding='utf-8') as f:
        case = json.load(f)

    # 2. โหลด System Prompt ของนักศึกษา
    prompt_file = "system_prompt.txt"
    system_prompt_text = ""
    if os.path.exists(prompt_file):
        with open(prompt_file, "r", encoding="utf-8") as pf:
            system_prompt_text = pf.read()
    else:
        # Fallback ในกรณีที่นักศึกษายังไม่ได้สร้างไฟล์
        system_prompt_text = "You are a helpful department recommendation system."

    # 3. รันโมเดล LLM
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": build_prompt(case, system_prompt_text)}],
        format="json",
    )

    # 4. จัดเตรียมผลลัพธ์
    result = json.loads(response.message.content)
    result["scenario_id"] = case["scenario_id"]
    return result

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <case.json>", file=sys.stderr)
        sys.exit(1)
        
    # พ่นผลลัพธ์ออกไปให้ bash / eval.py ใช้งานต่อ (ensure_ascii=False เพื่อไม่ให้ภาษาไทยกลายเป็น \u0e...)
    print(json.dumps(run(sys.argv[1]), ensure_ascii=False))