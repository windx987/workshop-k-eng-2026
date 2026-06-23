import sys
import json
import ollama

MODEL = "gemma4:12b"

def evaluate_student_prompt(prompt_text: str) -> dict:
    # Meta-prompt: คำสั่งที่ได้รับการปรับปรุงให้ strict และ dynamic ยิ่งขึ้น
    judge_prompt = f"""You are an expert Prompt Engineering Evaluator.
Your task is to dynamically grade a system prompt written by a student based on 5 core dimensions.

Be encouraging, constructive, and friendly in your analysis, highlighting what they did well first.

Grading Rubric (0-20 points dynamic scale for each):
1. Role: 0 = Missing, 1-10 = Vague, 11-20 = Clear persona with explicit context.
2. Framework: 0 = Missing, 1-10 = Mentioned but not enforced, 11-20 = Strictly structures logic (e.g., SWOT/Ikigai).
3. Task Breakdown: 0 = Single messy paragraph, 1-10 = Partial steps, 11-20 = Complete logical step-by-step instructions.
4. Empathy & Tone: 0 = Robotic/Missing, 1-10 = Basic politeness, 11-20 = Explicit commands to use positive reinforcement and empathy.
5. Format: 0 = Unspecified, 1-10 = Generic formatting, 11-20 = Precise schema enforcement (JSON keys, escape rules).

Student's System Prompt to evaluate:
\"\"\"
{prompt_text}
\"\"\"

Respond ONLY with a valid JSON object in this exact format. Do not include markdown code blocks (```json) or any outside conversational text:
{{
  "overall_critique": "A warm, encouraging paragraph in Thai describing how good or promising this prompt is, highlighting its key strengths first.",
  "criteria_scores": {{
    "role": 0,
    "framework": 0,
    "task_breakdown": 0,
    "tone": 0,
    "format": 0
  }},
  "total_score": 0,
  "feedback_summary": "Actionable advice in Thai on what specific missing details to add next to maximize their score."
}}
"""
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[{"role": "user", "content": judge_prompt}],
            format="json", # บังคับให้ Ollama พ่น JSON
        )
        
        # ถอดรหัสโครงสร้างข้อความ JSON
        result = json.loads(response.message.content)
        return result
        
    except (json.JSONDecodeError, Exception):
        # หากโครงสร้าง JSON เสียหาย ให้คะแนนเป็น 0 ทันที และไม่มีอธิบายข้อความยาวๆ เพื่อไม่ให้บิวท์ระบบ CI รวน
        return {
            "overall_critique": "ไม่สามารถประเมินได้ เนื่องจากผลลัพธ์จากโมเดลไม่อยู่ในรูปแบบ JSON ที่ถูกต้อง",
            "criteria_scores": {
                "role": 0,
                "framework": 0,
                "task_breakdown": 0,
                "tone": 0,
                "format": 0
            },
            "total_score": 0,
            "feedback_summary": "System Prompt ทำให้โครงสร้างเอาต์พุตของโมเดลแตกกรอบ"
        }

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python prompt_judge.py <system_prompt.txt>", file=sys.stderr)
        sys.exit(1)

    # อ่านไฟล์พรอมต์ของนักศึกษา
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        system_prompt = f.read()

    evaluation_result = evaluate_student_prompt(system_prompt)
    print(json.dumps(evaluation_result, ensure_ascii=False, indent=2))