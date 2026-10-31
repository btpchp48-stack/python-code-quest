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

# คลังคำถาม 5 ด่าน (รวม 15 ข้อ)
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
            "question": "ฟังก์ชัน any([False, 0, True]) จะส่งคืนค่าใด?",
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

# ฟังก์ชันประเมินระดับคะแนนพร้อมข้อความติดตลก (6 ระดับ)
def get_rank_message(score):
    if score == 150:
        return "🏆 ระดับ: เทพเจ้า Python ไร้เทียมทาน\n\n\"โอ้โห นี่มันอนาคตนักเขียนโค้ดมือหนึ่งของโลก! บอร์ดบริหาร Google กำลังเตรียมเก้าอี้รอคุณอยู่!\""
    elif score >= 120:
        return "🥇 ระดับ: เซียนบั๊ก ผู้ไร้พ่าย\n\n\"เก่งระดับนี้ ภาษา Python นึกว่าคุณเป็นคนคิดค้นเองซะอีก! นั่งชิวส่งอาจารย์ได้เลย!\""
    elif score >= 90:
        return "🥈 ระดับ: โปรแกรมเมอร์สายสู้ชีวิต\n\n\"รอดมาได้แบบเท่ๆ โค้ดผ่าน รันผ่าน สมองก็เกือบผ่านเหมือนกัน! ทำได้ดีมาก!\""
    elif score >= 60:
        return "🥉 ระดับ: นักรบ StackOverflow\n\n\"พอตัวอยู่นะ! ถือว่าเอาตัวรอดได้ แม้บางข้อจะใช้ดวงนำทางไปบ้างก็เหอะ!\""
    elif score >= 30:
        return "⚠️ ระดับ: โค้ดติด Error สายตาเริ่มพร่ามัว\n\n\"เกือบขิต! กาข้อไหนไปบ้างยังจำไม่ได้เลยใช่ไหมเนี่ย? ไปพักจิบกาแฟแล้วมาซ่อมด่วน!\""
    else:
        return "☠️ ระดับ: สลบคาคีย์บอร์ด\n\n\"แม่บอกแล้วไง อย่าหลับตอนเรียนน่ะ!! ตื่นมาอ่านเฉลยเดี๋ยวนี้เลยนะ!\""

# กำหนด Session State
if "level" not in st.session_state:
    st.session_state.level = 1
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "answered" not in st.session_state:
    st.session_state.answered = False
if "show_review" not in st.session_state:
    st.session_state.show_review = False

# รีเฟรชหน้าจออัตโนมัติเพื่ออัปเดตเวลา
if not st.session_state.game_over and not st.session_state.answered:
    st_autorefresh(interval=1000, key="timer_refresh")

st.title("🐍 Python Code Quest")
st.caption("เกมทบทวนความรู้ภาษา Python สำหรับนิสิต")

# ==========================================
# 1. หน้าจบเกม / สรุปคะแนน / ดูเฉลย
# ==========================================
if st.session_state.level > 5 or st.session_state.game_over:
    if st.session_state.show_review:
        # หน้าดูเฉลยคำตอบย้อนหลัง
        st.subheader("📖 เฉลยคำตอบและเหตุผลทั้งหมด")
        for lvl in range(1, 6):
            with st.expander(f"🚩 ด่านที่ {lvl}", expanded=True):
                for idx, q in enumerate(QUESTIONS_BANK[lvl], 1):
                    st.markdown(f"**ข้อ {idx}: {q['question']}**")
                    st.success(f"✅ **คำตอบที่ถูกต้อง:** ข้อ {q['answer']}. {q['choices'][q['answer']]}")
                    st.info(f"💡 **เหตุผล:** {q['explanation']}")
                    st.divider()
        
        if st.button("🔙 ย้อนกลับไปหน้าบอกคะแนน", type="primary", use_container_width=True):
            st.session_state.show_review = False
            st.rerun()
    else:
        # หน้าสรุปคะแนน
        st.balloons()
        st.success("🎉 ยินดีด้วย! คุณเล่นเกมจบเรียบร้อยแล้ว")
        st.metric(label="🏆 คะแนนรวมทั้งหมด", value=f"{st.session_state.total_score} / 150 คะแนน")
        
        # แสดงระดับคะแนน
        rank_msg = get_rank_message(st.session_state.total_score)
        st.info(rank_msg)
        
        col_rev, col_restart = st.columns(2)
        with col_rev:
            if st.button("📖 ดูเฉลยคำตอบทั้งหมด", use_container_width=True):
                st.session_state.show_review = True
                st.rerun()
        with col_restart:
            if st.button("🔄 เริ่มเล่นใหม่อีกครั้ง", type="primary", use_container_width=True):
                st.session_state.level = 1
                st.session_state.q_index = 0
                st.session_state.total_score = 0
                st.session_state.attempts = 0
                st.session_state.start_time = time.time()
                st.session_state.game_over = False
                st.session_state.answered = False
                st.session_state.show_review = False
                st.rerun()
    st.stop()

# ==========================================
# 2. ตัวนับเวลาด่านละ 2 นาที (120 วินาที)
# ==========================================
time_limit = 120
elapsed_time = time.time() - st.session_state.start_time
remaining_time = max(0, int(time_limit - elapsed_time))

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🚩 ด่านที่", f"{st.session_state.level} / 5")
with col2:
    st.metric("⏱️ เวลาที่เหลือ", f"{remaining_time} วิ")
with col3:
    st.metric("⭐ คะแนนรวม", st.session_state.total_score)

st.progress(remaining_time / time_limit)

# กรณีหมดเวลาในด่านนี้ (เปลี่ยนด่านให้อัตโนมัติ)
if remaining_time <= 0 and not st.session_state.answered:
    st.error("⏰ หมดเวลาสำหรับด่านนี้แล้ว! กำลังนำคุณไปยังด่านถัดไป...")
    time.sleep(3)
    st.session_state.level += 1
    st.session_state.q_index = 0
    st.session_state.attempts = 0
    st.session_state.start_time = time.time()
    st.rerun()

# ==========================================
# 3. แสดงข้อคำถามและการตอบ
# ==========================================
current_level_questions = QUESTIONS_BANK[st.session_state.level]
q_data = current_level_questions[st.session_state.q_index]

st.markdown("---")
st.subheader(f"ข้อที่ {st.session_state.q_index + 1} / {len(current_level_questions)}")
st.markdown(f"### {q_data['question']}")

choices = q_data['choices']
for key in ["A", "B", "C", "D"]:
    button_label = f"{key}. {choices[key]}"
    if st.button(button_label, key=f"btn_{key}", disabled=st.session_state.answered, use_container_width=True):
        if key == q_data['answer']:
            score_earned = 10 - (st.session_state.attempts * 2)
            st.session_state.total_score += score_earned
            st.success(f"✨ ถูกต้องครับ! คุณได้รับ +{score_earned} คะแนน")
            st.info(f"💡 **คำอธิบาย:** {q_data['explanation']}")
            st.session_state.answered = True
            st.toast("กำลังไปข้อถัดไปอัตโนมัติ...", icon="⏳")
            st.rerun()
        else:
            st.session_state.attempts += 1
            if st.session_state.attempts < 3:
                st.error(f"❌ ยังไม่ถูกต้อง! ตอบผิดไปแล้ว {st.session_state.attempts} ครั้ง (เหลือโอกาสอีก {3 - st.session_state.attempts} ครั้ง)")
            else:
                st.session_state.answered = True
                st.toast("กำลังไปข้อถัดไปอัตโนมัติ...", icon="⏳")
                st.rerun()

# ==========================================
# 4. แสดงเฉลยค้างไว้ 4 วินาที แล้วข้ามข้อให้อัตโนมัติ
# ==========================================
if st.session_state.answered:
    if st.session_state.attempts >= 3:
        st.error("❌ ตอบผิดครบ 3 ครั้งแล้ว คุณไม่ได้คะแนนในข้อนี้")
        st.warning(f"🔑 **คำตอบที่ถูกต้องคือข้อ {q_data['answer']}. {choices[q_data['answer']]}**")
        st.info(f"💡 **เหตุผลเฉลยอย่างละเอียด:** {q_data['explanation']}")
    
    st.caption("⏳ ระบบกำลังเปลี่ยนไปข้อถัดไปให้อัตโนมัติใน 4 วินาที...")
    time.sleep(4)  # ค้างหน้าเฉลยนานขึ้น (4 วินาที) ให้ผู้อ่านเข้าใจ
    
    # อัปเดตเพื่อไปยังข้อถัดไป หรือด่านถัดไป
    st.session_state.q_index += 1
    st.session_state.attempts = 0
    st.session_state.answered = False
    
    if st.session_state.q_index >= len(current_level_questions):
        st.session_state.level += 1
        st.session_state.q_index = 0
        st.session_state.start_time = time.time()
        
    st.rerun()
