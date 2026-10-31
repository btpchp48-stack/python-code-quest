import streamlit as st
# (นำโค้ดภาษา Python ในข้อ 3 มาวางทั้งหมดตรงนี้)

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

# คลังคำถาม 5 ด่าน
QUESTIONS_BANK = {
    1: [
        {
            "question": "ข้อใดต่อไปนี้ตั้งชื่อตัวแปรใน Python ไม่ถูกต้อง?",
            "choices": {"A": "my_var", "B": "2variable", "C": "_data", "D": "user_name1"},
            "answer": "B",
            "explanation": "ภาษา Python ห้ามนำหน้าชื่อตัวแปรด้วยตัวเลข (2variable จึงไม่ถูกต้อง)"
        },
        {
            "question": "ผลลัพธ์ของ print(type(5 / 2)) คือข้อใด?",
            "choices": {"A": "<class 'int'>", "B": "<class 'float'>", "C": "<class 'str'>", "D": "<class 'bool'>"},
            "answer": "B",
            "explanation": "การหารด้วยเครื่องหมาย / ใน Python 3 จะคืนค่าเป็น float เสมอ (ได้ 2.5)"
        },
        {
            "question": "ตัวดำเนินการใดใช้สำหรับหาเศษจากการหาร (Modulus)?",
            "choices": {"A": "//", "B": "/", "C": "%", "D": "**"},
            "answer": "C",
            "explanation": "เครื่องหมาย % ใช้คำนวณหาเศษจากการหาร"
        }
    ],
    2: [
        {
            "question": "ผลลัพธ์ของ 5 > 3 and 2 > 8 คืออะไร?",
            "choices": {"A": "True", "B": "False", "C": "None", "D": "Error"},
            "answer": "B",
            "explanation": "ตัวเชื่อม and จะเป็น True เมื่อเงื่อนไขทั้งสองข้างเป็น True (แต่ 2 > 8 เป็น False)"
        },
        {
            "question": "คำสั่งใดใช้ในการรับค่าข้อมูลจากผู้ใช้ทางคีย์บอร์ด?",
            "choices": {"A": "get()", "B": "read()", "C": "input()", "D": "scan()"},
            "answer": "C",
            "explanation": "ฟังก์ชัน input() ใช้สำหรับรับข้อความจากผู้ใช้"
        },
        {
            "question": "ผลลัพธ์ของ bool('') (ข้อความว่าง) คือข้อใด?",
            "choices": {"A": "True", "B": "False", "C": "None", "D": "Error"},
            "answer": "B",
            "explanation": "String ว่าง ('') เมื่อแปลงเป็น Boolean จะได้ค่าเป็น False"
        }
    ],
    3: [
        {
            "question": "คำสั่ง range(1, 5) จะส่งคืนชุดตัวเลขใด?",
            "choices": {"A": "1, 2, 3, 4, 5", "B": "1, 2, 3, 4", "C": "0, 1, 2, 3, 4", "D": "0, 1, 2, 3, 4, 5"},
            "answer": "B",
            "explanation": "range(start, stop) จะทำงานถึงค่า stop - 1 จึงได้ 1 ถึง 4"
        },
        {
            "question": "คำสั่งใดใช้หยุดการทำงานของ Loop ทันที?",
            "choices": {"A": "exit", "B": "stop", "C": "break", "D": "continue"},
            "answer": "C",
            "explanation": "break ใช้สำหรับออกจากคำสั่งวนซ้ำทันที"
        },
        {
            "question": "ผลลัพธ์ของ sum(range(1, 4)) คือข้อใด?",
            "choices": {"A": "6", "B": "10", "C": "4", "D": "3"},
            "answer": "A",
            "explanation": "range(1, 4) คือ [1, 2, 3] ผลรวมคือ 1 + 2 + 3 = 6"
        }
    ],
    4: [
        {
            "question": "ฟังก์ชันสร้างด้วยคีย์เวิร์ดใดใน Python?",
            "choices": {"A": "function", "B": "def", "C": "define", "D": "func"},
            "answer": "B",
            "explanation": "ภาษา Python ใช้คีย์เวิร์ด def ในการนิยามฟังก์ชัน"
        },
        {
            "question": "ฟังก์ชัน any([False, Zero, True]) จะส่งคืนค่าใด?",
            "choices": {"A": "False", "B": "True", "C": "None", "D": "Error"},
            "answer": "B",
            "explanation": "any() คืนค่า True หากมีสมาชิกใน Iterable เป็นจริงอย่างน้อย 1 ตัว"
        },
        {
            "question": "หากไม่ได้ระบุคำสั่ง return ในฟังก์ชัน ฟังก์ชันจะคืนค่าใดออกมารับ?",
            "choices": {"A": "0", "B": "False", "C": "None", "D": "Error"},
            "answer": "C",
            "explanation": "ฟังก์ชันที่ไม่มี return จะคืนค่า None โดยอัตโนมัติ"
        }
    ],
    5: [
        {
            "question": "การลบข้อมูลใน List โดยระบุ Index ใช้คำสั่งใด?",
            "choices": {"A": "list.remove()", "B": "list.pop()", "C": "list.clear()", "D": "list.delete()"},
            "answer": "B",
            "explanation": "pop(index) ลบข้อมูลตามตำแหน่ง Index (ถ้าไม่ใส่ตำแหน่งจะลบตัวสุดท้าย)"
        },
        {
            "question": "ข้อใดเป็นโครงสร้างข้อมูลชนิด Immutable (แก้ไขสมาชิกไม่ได้)?",
            "choices": {"A": "List", "B": "Dictionary", "C": "Tuple", "D": "Set"},
            "answer": "C",
            "explanation": "Tuple เมื่อสร้างแล้วจะไม่สามารถแก้ไข เพิ่ม หรือลดสมาชิกได้"
        },
        {
            "question": "ข้อใดคืนค่าความยาวหรือจำนวนสมาชิกของ List?",
            "choices": {"A": "list.size()", "B": "count(list)", "C": "len(list)", "D": "list.length()"},
            "answer": "C",
            "explanation": "ฟังก์ชัน len() ใช้หาจำนวนสมาชิกในโครงสร้างข้อมูล"
        }
    ]
}

# กำหนดค่าเริ่มต้น Session State
if "level" not in st.session_state:
    st.session_state.level = 1
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "level_score" not in st.session_state:
    st.session_state.level_score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "answered" not in st.session_state:
    st.session_state.answered = False

# รีเฟรชหน้าจอทุกๆ 1 วินาทีเพื่ออัปเดตเวลา
if not st.session_state.game_over:
    st_autorefresh(interval=1000, key="timer_refresh")

st.title("🐍 Python Code Quest")
st.caption("เกมทบทวนความรู้ภาษา Python สำหรับนิสิต")

# ตรวจสอบการจบเกม
if st.session_state.level > 5 or st.session_state.game_over:
    st.balloons()
    st.success("🎉 ยินดีด้วย! คุณเล่นเกมจบเรียบร้อยแล้ว")
    st.metric(label="🏆 คะแนนรวมทั้งหมด", value=f"{st.session_state.total_score} / 150 คะแนน")
    
    if st.button("🔄 เริ่มเล่นใหม่อีกครั้ง", use_container_width=True):
        st.session_state.level = 1
        st.session_state.q_index = 0
        st.session_state.total_score = 0
        st.session_state.level_score = 0
        st.session_state.attempts = 0
        st.session_state.start_time = time.time()
        st.session_state.game_over = False
        st.session_state.answered = False
        st.rerun()
    st.stop()

# คำนวณเวลานับถอยหลัง (120 วินาที / ด่าน)
time_limit = 120
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(0, int(time_limit - elapsed_time))

# แสดงสถานะด่านและเวลา
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🚩 ด่านที่", f"{st.session_state.level} / 5")
with col2:
    st.metric("⏱️ เวลาที่เหลือ", f"{remaining_time} วิ")
with col3:
    st.metric("⭐ คะแนนรวม", st.session_state.total_score)

st.progress(remaining_time / time_limit)

# หากหมดเวลาในด่านนี้
if remaining_time <= 0:
    st.warning("⏰ หมดเวลาสำหรับด่านนี้แล้ว! กำลังเปลี่ยนไปยังด่านถัดไป...")
    time.sleep(2)
    st.session_state.level += 1
    st.session_state.q_index = 0
    st.session_state.attempts = 0
    st.session_state.start_time = time.time()
    st.session_state.answered = False
    st.rerun()

# แสดงคำถามปัจจุบัน
current_level_questions = QUESTIONS_BANK[st.session_state.level]
q_data = current_level_questions[st.session_state.q_index]

st.markdown("---")
st.subheader(f"ข้อที่ {st.session_state.q_index + 1} / {len(current_level_questions)}")
st.markdown(f"**{q_data['question']}**")

# ปุ่มตัวเลือก A, B, C, D (ปุ่มใหญ่รองรับนิ้วกดบนมือถือ)
choices = q_data['choices']
for key in ["A", "B", "C", "D"]:
    button_label = f"{key}. {choices[key]}"
    if st.button(button_label, key=f"btn_{key}", disabled=st.session_state.answered, use_container_width=True):
        if key == q_data['answer']:
            score_earned = 10 - (st.session_state.attempts * 2)
            st.session_state.total_score += score_earned
            st.session_state.level_score += score_earned
            st.success(f"✨ ถูกต้องครับ! ได้รับ +{score_earned} คะแนน")
            st.info(f"💡 **เหตุผล:** {q_data['explanation']}")
            st.session_state.answered = True
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts < 3:
                st.error(f"❌ ยังไม่ถูกต้อง! ตอบผิดไปแล้ว {st.session_state.attempts} ครั้ง (เหลือโอกาสอีก {3 - st.session_state.attempts} ครั้ง)")
            else:
                st.error("❌ ตอบผิดครบ 3 ครั้งแล้ว คุณไม่ได้คะแนนในข้อนี้")
                st.info(f"🔑 **คำตอบที่ถูกต้องคือข้อ {q_data['answer']}**\n\n💡 **เหตุผล:** {q_data['explanation']}")
                st.session_state.answered = True

# ปุ่มไปข้อถัดไป
if st.session_state.answered:
    if st.button("ข้อถัดไป ➡️", type="primary", use_container_width=True):
        st.session_state.q_index += 1
        st.session_state.attempts = 0
        st.session_state.answered = False
        
        # เมื่อทำครบทุกข้อในด่าน
        if st.session_state.q_index >= len(current_level_questions):
            st.session_state.level += 1
            st.session_state.q_index = 0
            st.session_state.start_time = time.time()
            
        st.rerun()
