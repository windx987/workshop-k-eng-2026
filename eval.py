import sys
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ฐานข้อมูลภายในสำหรับตรวจจริตและบริบทอ้างอิงเฉพาะเจาะจงราย Persona (10 Custom Personas)
PERSONA_GT_EXTENDED = {
    "P01": {
        "name": "โรส",
        "must_have": ["คอม", "it", "ux", "ui", "สไลด์", "จัดหน้า"],
        "must_not": ["หมอ", "แพทย์", "เภสัช", "นิเทศ", "การตลาด", "วาดรูป"],
        "gt_context": "แนะแนวคณะสาย Tech/Design เช่น UX/UI Design หรือวิทยาการคอมพิวเตอร์ วิเคราะห์ตามหลัก SWOT มีการชมเรื่องการจัดหน้าสไลด์สวยงาม"
    },
    "P02": {
        "name": "แก้ว",
        "must_have": ["ภาษา", "อักษร", "มนุษย์", "คอนเทนต์", "บรรณาธิการ"],
        "must_not": ["วิศวะ", "บัญชี", "การเงิน", "คอม", "it"],
        "gt_context": "แนะนำคณะสายมนุษยศาสตร์ อักษรศาสตร์ หรือสาขา Content Creator ชมทักษะการจับประเด็นสรุปข้อมูลยาวๆ ให้สั้นกระชับเข้าใจง่าย"
    },
    "P03": {
        "name": "นาย",
        "must_have": ["data", "สถิติ", "วิเคราะห์", "คณิต", "คอม"],
        "must_not": ["การตลาด", "เซลส์", "ประชาสัมพันธ์", "ประวัติศาสตร์"],
        "gt_context": "คณะที่ตอบโจทย์คือ Data Science หรือ สถิติประยุกต์ ชมทักษะการคำนวณและสถิติจากการแกะ Stats เกมและเปิด Excel พลอตกราฟ"
    },
    "P04": {
        "name": "บาส",
        "must_have": ["วิศวะ", "คอมพิวเตอร์", "ฮาร์ดแวร์", "เทคโนโลยี", "ซ่อม"],
        "must_not": ["การโรงแรม", "ท่องเที่ยว", "ภาษา", "อักษร"],
        "gt_context": "แนะนำ วิศวกรรมคอมพิวเตอร์ หรือ เทคโนโลยีคอมพิวเตอร์ ชมทักษะการเป็นช่างจากการแกะซ่อมคอมและจัดสายไฟเนี๊ยบๆ"
    },
    "P05": {
        "name": "มิ้นท์",
        "must_have": ["กราฟิก", "ศิลปกรรม", "นวัตกรรมสื่อ", "ออกแบบ"],
        "must_not": ["บัญชี", "การเงิน", "คณิต", "วิศวะ"],
        "gt_context": "แนะนำคณะสาย ดิจิทัลมีเดีย, กราฟิกดีไซน์ หรือ นวัตกรรมสื่อสารสังคม ชมเซนส์ศิลปะและการคุมโทนภาพกราฟิกไดคัทรูป"
    },
    "P06": {
        "name": "เป้",
        "must_have": ["ตัดต่อ", "editor", "ภาพยนตร์", "ดิจิทัลมีเดีย"],
        "must_not": ["เคมี", "ฟิสิกส์", "วิศวะ", "หมอ"],
        "gt_context": "คณะที่เหมาะคือ นิเทศศาสตร์ สาขาการตัดต่อ หรือ ดิจิทัลมีเดีย ชมทักษะการเล่าเรื่องด้วยภาพและการจัดจังหวะซาวด์เอฟเฟกต์"
    },
    "P07": {
        "name": "ป้อน",
        "must_have": ["อักษร", "มนุษย์", "สารสนเทศ", "บรรณารักษ์"],
        "must_not": ["พละ", "นิเทศ", "การตลาด", "การแสดง"],
        "gt_context": "แนะนำคณะสาย สารสนเทศศาสตร์, อักษรศาสตร์ หรือ บรรณารักษ์ยุคดิจิทัล ชมความเป็นนักรีเสิร์ชชั้นยอดและการสืบค้นข้อมูล"
    },
    "P08": {
        "name": "คีน",
        "must_have": ["คอม", "ฟินเทค", "fintech", "บล็อคเชน", "it"],
        "must_not": ["ชีววิทยา", "พยาบาล", "การโรงแรม", "ท่องเที่ยว"],
        "gt_context": "แนะนำคณะวิทยาการคอมพิวเตอร์ (สาย FinTech) หรือวิศวกรรมการเงิน ชมความถนัดเรื่องตรรกะคณิตศาสตร์ที่อินเรื่อง Crypto และ AI"
    },
    "P09": {
        "name": "นัท",
        "must_have": ["ดนตรี", "เทคโนโลยีดนตรี", "sound", "นิเทศ"],
        "must_not": ["คณิต", "บัญชี", "เคมี", "วิศวะโครงสร้าง"],
        "gt_context": "คณะที่ตรงสุดคือ ดุริยางคศาสตร์ สาขาเทคโนโลยีดนตรี หรือ Sound Engineer ชมความถนัดด้านการแยกแยะคลื่นเสียงและมิกซ์เพลง"
    },
    "P10": {
        "name": "วิว",
        "must_have": ["บัญชี", "การเงิน", "สถิติ", "บริหาร"],
        "must_not": ["ศิลปกรรม", "สถาปัตยศาสตร์", "ดนตรี", "นิเทศ"],
        "gt_context": "แนะนำคณะพาณิชยศาสตร์และการบัญชี หรือ สาขาการเงิน ชมระเบียบวินัยเชิงตัวเลขและการคุมงบประมาณจัดตาราง Google Sheets"
    }
}

def calc_text_similarity(text1: str, text2: str) -> float:
    try:
        # ใช้ char_wb vectorizer เพื่อรองรับโครงสร้างประโยคภาษาไทยที่ไม่มีการแบ่งเว้นวรรคคำชัดเจน
        v = TfidfVectorizer(analyzer='char_wb', ngram_range=(2, 4))
        tfidf = v.fit_transform([text1.lower().strip(), text2.lower().strip()])
        return float(cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0])
    except Exception:
        return 0.0

def evaluate_strict(case_path: str, response_path: str) -> dict:
    with open(case_path, encoding='utf-8') as f:
        case = json.load(f)
    with open(response_path, encoding='utf-8') as f:
        response = json.load(f)

    # 1. ตรวจสอบความถูกต้องของแผนก/คณะเรียน (เกณฑ์เดิมแบบ Exact Match)
    gt = set(case["gt_departments"])
    predicted = set(response.get("recommended_departments", []))
    correct = len(gt & predicted)
    total_gt = len(gt)
    base_score = (correct / total_gt) if total_gt > 0 else 0.0

    # ดึงค่าคำตอบดิบและไอดีเพื่อมาคำนวณแบบ Strict เพิ่มเติม
    scenario_id = case["scenario_id"]
    raw_text = response.get("raw_output", "") # แนะนำให้นักศึกษาเก็บข้อความเต็มจากโมเดลไว้ที่ Key นี้ในตัวแปร JSON
    
    # หากไม่มีการส่งคีย์ raw_output มา ให้ใช้การดึงค่าพารามิเตอร์ทั้งหมดมาสแกนแทนชั่วคราว
    if not raw_text:
        raw_text = json.dumps(response, ensure_ascii=False)

    # --------------------------------------------------------
    # เพิ่มระบบ Strict Checklists (วิเคราะห์การออกแบบ Prompt ของเด็ก)
    # --------------------------------------------------------
    checklist = {}
    
    # Check 1: Empathy & Positive Feedback (ต้องแสดงความเข้าอกเข้าใจและดึงจุดแข็งมาชม)
    has_empathy = any(w in raw_text for w in ["เข้าใจ", "กังวล", "เครียด", "ไม่เป็นไร", "สบายใจ", "จุดแข็ง", "ชื่นชม"])
    checklist["empathy_and_positive_tone"] = "PASS" if has_empathy else "FAIL"

    # Check 2: Framework/Theory Enforcement (ตรวจสอบว่าโมเดลได้ใช้ทฤษฎีคิดวิเคราะห์ตามเงื่อนไขหลักไหม)
    has_framework = any(w in raw_text.lower() for w in ["swot", "ikigai", "holland", "ทฤษฎี", "framework"])
    checklist["framework_execution"] = "PASS" if has_framework else "FAIL"

    # Check 3: Persona Custom Validation (สแกนตรวจคำค้นหาบังคับและคำต้องห้ามของแต่ละ Persona)
    persona_pass = True
    if scenario_id in PERSONA_GT_EXTENDED:
        db = PERSONA_GT_EXTENDED[scenario_id]
        # ต้องมีคำสำคัญตามจริตความถนัด
        has_must = any(w in raw_text.lower() for w in db["must_have"])
        # ห้ามหลุดคำแนะนำคณะต้องห้ามเด็ดขาด
        has_banned = any(w in raw_text.lower() for w in db["must_not"])
        
        if not has_must or has_banned:
            persona_pass = False
        
        # คำนวณความสอดคล้องทางบริบทโครงสร้างคำตอบผ่าน Cosine Similarity
        sim_score = calc_text_similarity(raw_text, db["gt_context"])
        checklist["semantic_similarity_match"] = f"{sim_score*100:.1f}%"
    else:
        checklist["semantic_similarity_match"] = "N/A"

    checklist["persona_style_and_rules"] = "PASS" if persona_pass else "FAIL"

    # --------------------------------------------------------
    # การคำนวณเกรดแบบถ่วงน้ำหนักความเข้มงวด (Strict Final Score)
    # --------------------------------------------------------
    # สูตร: คะแนนคณะ (60%) + คะแนนน้ำเสียง/ทฤษฎี (20%) + คะแนนควบคุมกฎฟิกซ์ประจำตัว (20%)
    bonus_score = 0.0
    if has_empathy: bonus_score += 0.1
    if has_framework: bonus_score += 0.1
    if persona_pass: bonus_score += 0.2
    
    final_score = round((base_score * 0.6) + bonus_score, 4)

    return {
        "scenario_id": scenario_id,
        "department_match_ratio": f"{correct}/{total_gt}",
        "checklists": checklist,
        "score": final_score
    }

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python eval.py <case.json> <response.json>", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(evaluate_strict(sys.argv[1], sys.argv[2]), ensure_ascii=False))