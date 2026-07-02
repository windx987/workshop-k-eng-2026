# เฟรมเวิร์คประเมินผล Prompt Engineering

เฟรมเวิร์คแบบ CI สำหรับประเมินความแม่นยำของ LLM ในเครื่อง ส่ง prompt ไปยังโมเดล Ollama และให้คะแนนผลลัพธ์เทียบกับคำตอบที่ถูกต้อง — ไม่ต้องใช้ API ภายนอก

<!-- ```
data/*.json  →  main.py  →  Ollama (gemma4:12b)  →  eval.py  →  คะแนน (0.0–1.0)
``` -->
![alt text](<ChatGPT Image Jun 26, 2026, 04_54_44 PM.png>)

## ความต้องการของระบบ

- **Windows 10 / 11**
- **Git for Windows** (รวม Git Bash)
- **Ollama**
- **Python 3.12+**

## การตั้งค่า LLM ในเครื่อง

### ติดตั้ง Ollama

```powershell
irm https://ollama.com/install.ps1 | iex
```

เปิด PowerShell ใหม่หลังติดตั้ง แล้วตรวจสอบ:

```powershell
ollama --version
```

### เริ่มต้น Ollama และดาวน์โหลดโมเดล

**แบบปกติ** — ดาวน์โหลดจาก Ollama registry:

```powershell
ollama pull gemma4:12b
ollama serve
```

โมเดลมีขนาด ~7.6 GB หากดาวน์โหลดหยุดกลางคัน ให้รัน `ollama pull gemma4:12b` ใหม่ — Ollama จะดาวน์โหลดต่อจากที่ค้างไว้

**แบบ Local** — คัดลอกโมเดลเข้าโปรเจกต์:

```powershell
Copy-Item -Recurse "$env:USERPROFILE\.ollama\models" .\models
```

จากนั้น serve จากโฟลเดอร์นั้น:

```powershell
$env:OLLAMA_MODELS = ".\models"
ollama serve
```

### แก้ปัญหาที่พบบ่อย

#### `ollama serve` ขึ้น "bind: Only one usage of each socket address"

มี Ollama อื่นใช้พอร์ต 11434 อยู่ ให้หยุดก่อน:

```powershell
Stop-Process -Name "ollama*" -Force
```

แล้วรัน `ollama serve` ใหม่

### ทดสอบโมเดล

เปิด terminal ใหม่ (ให้ `ollama serve` ทำงานอยู่) แล้วลองคุย:

```powershell
ollama run gemma4:12b
```

```
>>> hello
Hello! How can I help you today? 😊

>>> /bye
```

ถ้าโมเดลตอบได้ แสดงว่าพร้อมใช้งานแล้ว

## การติดตั้ง

### 1. ติดตั้ง Git for Windows

ต้องใช้ Git Bash เพื่อรัน `script.sh`

```powershell
winget install --id Git.Git --exact --source winget --silent --disable-interactivity --accept-source-agreements --accept-package-agreements
```

เปิด PowerShell ใหม่แล้วตรวจสอบ:

```powershell
git --version
```

ตั้งค่า alias `gbash` สำหรับ Git Bash:

```powershell
Set-Alias gbash "C:\Program Files\Git\bin\bash.exe"
gbash --version
```

> **หมายเหตุ:** alias นี้ใช้ได้เฉพาะ session นี้เท่านั้น ต้องรัน `Set-Alias` ใหม่ทุกครั้งที่เปิด PowerShell

สำหรับห้อง ECC 704:

```powershell
Set-Alias gbash "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
```

### 2. Clone repository

เปิด **PowerShell** หรือ **Git Bash**:

```powershell
git clone https://github.com/windx987/workshop-k-eng-2026.git
cd ./workshop-k-eng-2026
```

### 3. ติดตั้ง Python 3.12 (ถ้ายังไม่มี)

ตรวจสอบว่ามี Python แล้วหรือยัง:

```powershell
python --version
```

ถ้าได้ `Python 3.12.x` ขึ้นไป ข้ามไปขั้นตอนที่ 4 ได้เลย ถ้าไม่มีให้ติดตั้ง:

```powershell
winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
```

เปิด PowerShell ใหม่แล้วตรวจสอบ:

```powershell
python --version
```

ถ้ายังหา `python` ไม่เจอ ให้เพิ่ม path เหล่านี้ใน **Settings → System → Advanced system settings → Environment Variables → Path (User)**:

```
%USERPROFILE%\AppData\Local\Programs\Python\Python312
%USERPROFILE%\AppData\Local\Programs\Python\Python312\Scripts
```

แล้วเปิด terminal ใหม่และตรวจสอบอีกครั้ง

### 4. สร้าง virtual environment และติดตั้ง dependencies

```bash
python -m venv .venv
.venv/Scripts/pip.exe install -r requirements.txt
```

### 5. ทดสอบการติดตั้ง

```bash
.venv/Scripts/python.exe main.py data/S1.json
```

ควรเห็น JSON output ที่มี `recommended_departments` แสดงว่าพร้อมใช้งาน

## จุดเริ่มต้นด่วน

รันคำสั่งนี้ใน PowerShell เพื่อสร้างไฟล์ `system_prompt.txt` เริ่มต้น:

```powershell
echo "You are a university department advisor. Analyze the student's description carefully and recommend the most suitable departments. Be empathetic and encouraging in your response. Explain your reasoning clearly before making recommendations." > system_prompt.txt
```

จากนั้นเปิด `system_prompt.txt` ใน VS Code และปรับแต่งเพื่อให้ได้คะแนนสูงขึ้น

## การใช้งาน

รัน pipeline ประเมินทั้งหมด:

```powershell
gbash script.sh
```

เลือก mode ที่ต้องการ:

```powershell
gbash script.sh public   # เฉพาะเคสสาธารณะ (S1-S3)
gbash script.sh judge    # ประเมิน prompt เท่านั้น
```

รันเคสเดี่ยว:

```bash
.venv/Scripts/python.exe main.py data/S1.json
```

## Prompt Judge

เขียน system prompt ในไฟล์ `system_prompt.txt` แล้วรัน:

```powershell
gbash script.sh judge
```

## สร้าง Agent ของตัวเอง

เมื่อเขียน `system_prompt.txt` เสร็จแล้ว สามารถสร้างเป็นโมเดล Ollama ของตัวเองได้:

**1. สร้าง Modelfile จาก system prompt:**

```powershell
$prompt = Get-Content system_prompt.txt -Raw
$rule = "IMPORTANT: Respond ONLY with a valid JSON object. Do NOT include 'thought', 'reasoning', or any extra keys outside the JSON."
"FROM gemma4:12b`nSYSTEM `"$prompt`n`n$rule`"" | Out-File -Encoding utf8 Modelfile
```

**2. สร้าง agent:**

```powershell
ollama create agent-007 -f Modelfile
```

**3. ทดสอบ agent ใน chat mode:**

```powershell
ollama run agent-007
```

ตัวอย่างการใช้งาน:

```
>>> {"scenario_id": "demo", "student_text": "I enjoy building mobile apps and solving algorithm puzzles.", "allowed_departments": ["Computer Science", "UX/UI Design", "Data Science", "Business Administration"], "max_suggestions": 2}
{"scenario_id": "demo", "raw_output": "You clearly enjoy hands-on software work and analytical problem-solving...", "recommended_departments": ["Computer Science", "UX/UI Design"]}

>>> /bye
```
<!-- 
**4. รัน evaluation ด้วย agent ของตัวเอง หรือคุยใน chat mode:**

เปลี่ยน `MODEL` ใน `main.py` จาก `"gemma4:12b"` เป็น `"agent-007"` แล้วรัน:

```powershell
gbash script.sh
```

หรือจะคุยกับ agent โดยตรง:

```powershell
ollama run agent-007
```

**5. ลองใช้ agent กับเคสเพิ่มเติม:**

`data/own_agent/S4.json` และ `data/own_agent/S5.json` เป็นเคสเพิ่มเติมสำหรับทดสอบ agent ของตัวเองโดยเฉพาะ ไม่ได้อยู่ในชุดเคสสาธารณะ S1-S3:

```bash
.venv/Scripts/python.exe main.py data/own_agent/S4.json
.venv/Scripts/python.exe main.py data/own_agent/S5.json
```

> **เคล็ดลับ:** ทุกครั้งที่แก้ `system_prompt.txt` ให้รันขั้นตอนที่ 1–2 ใหม่เพื่อ rebuild agent -->
