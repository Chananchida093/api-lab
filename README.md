# API Testing Lab — QuickPizza

## 1. ภาพรวมของงาน

งานนี้เป็นการทดสอบ REST API ของ QuickPizza โดยใช้ Python, pytest และ requests เพื่อตรวจสอบการทำงานของ API ทั้งกรณีที่ข้อมูลถูกต้องและไม่ถูกต้อง รวมถึงการตรวจสอบสิทธิ์ผู้ใช้และการจัดการ Ratings

การทดสอบครอบคลุมการอ่านข้อมูล การสร้าง แก้ไข และลบ Ratings (CRUD) โดยตรวจสอบทั้ง HTTP Status Code และข้อมูล JSON ที่ตอบกลับจาก API

## 2. การออกแบบและดำเนินการทดสอบ

**Part 0 — API Testing Basics**

ทดลองเรียก API ด้วย curl และ Python จากนั้นเขียน Automated Tests สำหรับตรวจสอบข้อมูลพิซซ่า การเข้าสู่ระบบ การจัดการ Ratings และกรณีที่ API ต้องปฏิเสธคำขอ

ใช้ pytest Fixtures สร้างผู้ใช้และข้อมูลใหม่สำหรับแต่ละ Test เพื่อให้ทดสอบได้อย่างอิสระ และใช้ requests.Session เพื่อเก็บ Cookies ระหว่างการเรียก API

**Part A — Input Space Partitioning**

ออกแบบ Test Cases โดยแบ่งข้อมูลนำเข้าออกเป็นกลุ่มตามเงื่อนไขของ API และใช้ Base Choice Coverage เพื่อให้ครอบคลุมทุก Block โดยไม่ต้องทดสอบทุก Combination

### Input Domain Model — POST /api/ratings

| Characteristic | Block | Test Value | Test Name |
|---|---|---|---|
| C1: Value of stars | ต่ำกว่า 1 | 0 | `test_stars_out_of_range[0]` |
| | 1–5 (Base) | 3 | `test_base_choice_is_saved` |
| | มากกว่า 5 | 6 | `test_stars_out_of_range[6]` |
| C2: Type of stars | Integer (Base) | 3 | `test_base_choice_is_saved` |
| | Decimal | 3.5 | `test_decimal_stars_refused` |
| | Text | "3" | `test_text_stars_refused` |
| | Missing | ไม่ส่ง stars | `test_missing_stars_refused` |
| C3: Pizza | Exists (Base) | Valid Pizza ID | `test_base_choice_is_saved` |
| | Does not exist | 999999999 | `test_nonexistent_pizza_refused` |
| C4: Token | Own Token (Base) | Valid Token | `test_base_choice_is_saved` |
| | None | No Header | `test_no_token_refused` |
| | Wrong Length | token short | `test_short_token_refused` |

เลือก Base Choice เป็น Rating 3 ดาว, Pizza ID ที่มีอยู่จริง และ Token ของผู้ใช้ จากนั้นเปลี่ยนค่าทีละ Characteristic โดยคงค่าอื่นเป็น Base

- **Base Choice Coverage:** 9 Test Cases
- **All Combinations Coverage:** 72 Test Cases

### Boundary Value Testing

ทดสอบการแก้ไข Rating ด้วยค่า 0, 1, 5 และ 6 โดยค่าที่ถูกต้องต้องแก้ไขสำเร็จ ส่วนค่าที่ไม่ถูกต้องต้องถูกปฏิเสธและไม่ทำให้ข้อมูลเดิมเปลี่ยนแปลง

### Authorization Testing

สร้างผู้ใช้สองคนเพื่อทดสอบว่าผู้ใช้คนอื่นไม่สามารถอ่าน แก้ไข หรือลบ Rating ที่ไม่ได้เป็นเจ้าของได้ โดยตรวจสอบทั้ง Status Code และข้อมูลของเจ้าของหลังการทดสอบ

## 3. การติดตั้งและรันทดสอบ

โปรเจกต์ใช้ Python 3.10 ขึ้นไป โดยติดตั้ง Library จาก `requirements.txt` ด้วยคำสั่ง `pip install -r requirements.txt`

สามารถรัน Tests ทั้งหมดด้วย `pytest -v` และดูรายงานผลการทดสอบได้จากไฟล์ [report.html](report.html)

## 4. ผลการทดสอบ

ผลการทดสอบทั้งหมดจาก HTML Report:

| Result | จำนวน |
|---|---:|
| Passed | 32 |
| XFailed | 1 |
| Failed | 0 |

พบ Defect ในกรณีที่ผู้ใช้ยกเว้นเครื่องมือตัดพิซซ่าทั้งหมด โดย API ตอบกลับ HTTP 500 แทน HTTP 400 พร้อม Error Message ตามที่ควรจะเป็น จึงบันทึกกรณีนี้เป็น `xfail` เพื่อเก็บไว้ตรวจสอบเมื่อมีการแก้ไขระบบ

## 5. สรุป

การทดสอบครั้งนี้ครอบคลุม API พื้นฐาน การจัดการ Ratings การตรวจสอบข้อมูลนำเข้าและ Boundary Values รวมถึงสิทธิ์ในการเข้าถึงข้อมูล โดยใช้ Automated Tests ที่สามารถรันแยกกันได้

ผลการทดสอบหลักผ่านทั้งหมด 32 กรณี และมี Defect ที่บันทึกไว้เป็น Expected Failure จำนวน 1 กรณี

รายละเอียดผลการทดลอง Defect Report และคำตอบ Reflection อยู่ใน `RESULTS.md`
