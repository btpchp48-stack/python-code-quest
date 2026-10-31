import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh

# กำหนดค่าหน้าเว็บให้รองรับ Mobile Responsive
st.set_page_config(
    page_title="Python Code Quest",
    page_icon="🐍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# คลังคำถาม 5 ด่าน พร้อมคำอธิบายตัวเลือก (Choices) ทั้งหมด
QUESTIONS_BANK = {
    1: [
        {
            "question": "ข้อใดต่อไปนี้ตั้งชื่อตัวแปรใน Python ไม่ถูกต้อง?",
            "choices": {"A": "my_var", "B": "2variable", "C": "_data", "D": "user_name1"},
            "answer": "B",
            "explanation": "ภาษา Python ห้ามนำหน้าชื่อตัวแปรด้วยตัวเลข (2variable จึงไม่ถูกต้อง)",
            "choices_detail": {
                "A": "my_var: ถูกต้อง (ใช้ตัวอักษรและ underscore ได้)",
                "B": "2variable: ไม่ถูกต้อง (ห้ามขึ้นต้นด้วยตัวเลข)",
                "C": "_data: ถูกต้อง (ขึ้นต้นด้วย underscore ได้)",
                "D": "user_name1: ถูกต้อง (มีตัวเลขต่อท้ายได้)"
            }
        },
        {
            "question": "ผลลัพธ์ของ print(type(5 / 2)) คือข้อใด?",
            "choices": {"A": "<class 'int'>", "B": "<class 'float'>", "C": "<class 'str'>", "D": "<class 'bool'>"},
            "answer": "B",
            "explanation": "การหารด้วยเครื่องหมาย / ใน Python 3 จะคืนค่าเป็น float เสมอ (ได้ 2.5)",
            "choices_detail": {
                "A": "<class 'int'>: จำนวนเต็ม (เช่น 5, 2)",
                "B": "<class 'float'>: ทศนิยม (ผลหาร 5 / 2 = 2.5)",
                "C": "<class 'str'>: ข้อความ/สตริง",
                "D": "<class 'bool'>: ค่าความจริง (True/False)"
            }
        },
        {
            "question": "ตัวดำเนินการใดใช้สำหรับหาเศษจากการหาร (Modulus)?",
            "choices": {"A": "//", "B": "/", "C": "%", "D": "**"},
            "answer": "C",
            "explanation": "เครื่องหมาย % ใช้คำนวณหาเศษจากการหาร",
            "choices_detail": {
                "A": "// : หารเอาส่วน (Floor Division)",
                "B": "/ : หารได้ผลลัพธ์เป็นทศนิยม",
                "C": "% : หารเอาเศษ (Modulus)",
                "D": "** : ยกกำลัง (Exponentiation)"
            }
        }
    ],
    2: [
        {
            "question": "ผลลัพธ์ของ 5 > 3 and 2 > 8 คืออะไร?",
            "choices": {"A": "True", "B": "False", "C": "None", "D": "Error"},
            "answer": "B",
            "explanation": "ตัวเชื่อม and จะเป็น True เมื่อเงื่อนไขทั้งสองข้างเป็น True (แต่ 2 > 8 เป็น False)",
            "choices_detail": {
                "A": "True: เป็นจริงทั้งสองข้าง (ในข้อนี้ไม่ใช่)",
                "B": "False: เป็นเท็จเนื่องจาก 2 > 8 เป็น False",
                "C": "None: ค่าว่างเปล่า",
                "D": "Error: ข้อผิดพลาดทางไวยากรณ์"
            }
        },
        {
            "question": "คำสั่งใดใช้ในการรับค่าข้อมูลจากผู้ใช้ทางคีย์บอร์ด?",
            "choices": {"A": "get()", "B": "read()", "C": "input()", "D": "scan()"},
            "answer": "C",
            "explanation": "ฟังก์ชัน input() ใช้สำหรับรับข้อความจากผู้ใช้",
            "choices_detail": {
                "A": "get(): ใช้ดึงค่าจาก Dictionary หรือ HTTP Request",
                "B": "read(): ใช้ใช้อ่านไฟล์ข้อมูล",
                "C": "input(): รับข้อความจากผู้ใช้ทางคีย์บอร์ด",
                "D": "scan(): ไม่ใช่ฟังก์ชันมาตรฐานของ Python"
            }
        },
        {
            "question": "ผลลัพธ์ของ bool('') (ข้อความว่าง) คือข้อใด?",
            "choices": {"A": "True", "B": "False", "C": "None", "D": "Error"},
            "answer": "B",
            "explanation": "String ว่าง ('') เมื่อแปลงเป็น Boolean จะได้ค่าเป็น False",
            "choices_detail": {
                "A": "True: ข้อความที่มีตัวอักษรอย่างน้อย 1 ตัว",
                "B": "False: ข้อความว่างเปล่า ('')",
                "C": "None: ค่านัล/ค่าว่าง",
                "D": "Error: ไม่เกิดข้อผิดพลาด"
            }
        }
    ],
    3: [
        {
            "question": "คำสั่ง range(1, 5) จะส่งคืนชุดตัวเลขใด?",
            "choices": {"A": "1, 2, 3, 4, 5", "B": "1, 2, 3, 4", "C": "0, 1, 2, 3, 4", "D": "0, 1, 2, 3, 4, 5"},
            "answer": "B",
            "explanation": "range(start, stop) จะทำงานถึงค่า stop - 1 จึงได้ 1 ถึง 4",
            "choices_detail": {
                "A": "1, 2, 3, 4, 5 : เกินค่า stop มา 1 ตัว",
                "B": "1, 2, 3, 4 : ถูกต้อง (เริ่มจาก 1 ถึง 5-1)",
                "C": "0, 1, 2, 3, 4 : เริ่มจาก 0 (ไม่ใช่ 1)",
                "D": "0, 1, 2, 3, 4, 5 : เริ่มจาก 0 และรวมค่า stop"
            }
        },
        {
            "question": "คำสั่งใดใช้หยุดการทำงานของ Loop ทันที?",
            "choices": {"A": "exit", "B": "stop", "C": "break", "D": "continue"},
            "answer": "C",
            "explanation": "break ใช้สำหรับออกจากคำสั่งวนซ้ำทันที",
            "choices_detail": {
                "A": "exit: ปิดการทำงานของโปรแกรมทั้งหมด",
                "B": "stop: ไม่ใช่คีย์เวิร์ดใน Python",
                "C": "break: ออกจาก Loop ทันที",
                "D": "continue: ข้ามไปรอบถัดไปของ Loop"
            }
        },
        {
            "question": "ผลลัพธ์ของ sum(range(1, 4)) คือข้อใด?",
            "choices": {"A": "6", "B": "10", "C": "4", "D": "3"},
            "answer": "A",
            "explanation": "range(1, 4) คือ [1, 2, 3] ผลรวมคือ 1 + 2 + 3 = 6",
            "choices_detail": {
                "A": "6 : ผลบวกของ 1 + 2 + 3",
                "B": "10 : ผลบวกถึงเลข 4 (1+2+3+4)",
                "C": "4 : ค่าจุดหยุดของ range",
                "D": "3 : จำนวนสมาชิกใน range"
            }
        }
    ],
    4: [
        {
            "question": "ฟังก์ชันสร้างด้วยคีย์เวิร์ดใดใน Python?",
            "choices": {"A": "function", "B": "def", "C": "define", "D": "func"},
            "answer": "B",
            "explanation": "ภาษา Python ใช้คีย์เวิร์ด def ในการนิยามฟังก์ชัน",
            "choices_detail": {
                "A": "function: คีย์เวิร์ดในภาษา JavaScript",
                "B": "def: คีย์เวิร์ดมาตรฐานใน Python (มาจาก define)",
                "C": "define: คีย์เวิร์ดในภาษา C/C++",
                "D": "func: คีย์เวิร์ดในภาษา Go/Swift"
            }
        },
        {
            "question": "ฟังก์ชัน any([False, 0, True]) จะส่งคืนค่าใด?",
            "choices": {"A": "False", "B": "True", "C": "None", "D": "Error"},
            "answer": "B",
            "explanation": "any() คืนค่า True หากมีสมาชิกใน Iterable เป็นจริงอย่างน้อย 1 ตัว",
            "choices_detail": {
                "A": "False: คืนค่านี้เมื่อทุกตัวเป็น False เท
