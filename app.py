import streamlit as st
import psycopg2
import hashlib
import numpy as np
import requests

# Database connection URL
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Weighted Score Method (WSM) for study time allocation
def wsm_allocation(math, eng, sci, comp, soc, total_study_time):
    total_score = math + eng + sci + comp + soc
    weights = [(100 - math) / total_score, (100 - eng) / total_score, 
               (100 - sci) / total_score, (100 - comp) / total_score,
               (100 - soc) / total_score]
    study_times = np.array(weights) * total_study_time
    return {"Math": round(study_times[0], 2), "English": round(study_times[1], 2),
            "Science": round(study_times[2], 2), "Computer": round(study_times[3], 2),
            "Social Science": round(study_times[4], 2)}

# Google Drive PDF Links
pdf_drive_links = {
    "10th_Computer": "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp",
    "10th_Mathematics": "1g83nbaDLFtUYBW46uWqZSxF6kKGCnoEk",
    "10th_Science": "1Z5Lh-v0lzHZ6tc-SZFZGJQsbykeCW57P",
    "10th_English": "1qYkk7srJSnfzSQahhdcSGFbZ48uptr_d",
    "10th_Social Science": "1fqQlgUs6f8V4CMEEkFxM6lDLHi3FePpq"
}

def get_pdf_viewer_link(file_id):
    return f"https://drive.google.com/file/d/{file_id}/preview"

def get_advanced_quiz():
    api_url = "https://gemi-api-url.com/generate-quiz"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json().get('quiz_questions', [])
    return ["Unable to fetch advanced quiz."]

st.title("📚 Student Learning App")

# Student Registration Form
with st.form("registration_form"):
    name = st.text_input("👤 Name", max_chars=100)
    password = st.text_input("🔑 Password", type="password", max_chars=255)
    mobile_number = st.text_input("📱 Mobile Number", max_chars=20)
    email = st.text_input("📧 Email", max_chars=100)
    class_name = st.text_input("🏫 Class", max_chars=10)
    age = st.number_input("🎂 Age", min_value=1, max_value=100, step=1)
    gender = st.selectbox("⚧️ Gender", ["Male", "Female", "Other"])
    math = st.number_input("📐 Math Score", min_value=0, max_value=100, step=1)
    english = st.number_input("📖 English Score", min_value=0, max_value=100, step=1)
    science = st.number_input("🔬 Science Score", min_value=0, max_value=100, step=1)
    computer = st.number_input("💻 Computer Score", min_value=0, max_value=100, step=1)
    social_science = st.number_input("🌍 Social Science Score", min_value=0, max_value=100, step=1)
    study_time = st.number_input("⏳ Study Time (hours per day)", min_value=0.0, max_value=24.0, step=0.1)
    submitted = st.form_submit_button("🚀 Register")

if submitted:
    if not name or not password or not mobile_number or not email:
        st.error("⚠️ Please fill in all required fields.")
    else:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            hashed_password = hash_password(password)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100), password VARCHAR(255), mobile_number VARCHAR(20),
                    email VARCHAR(100) UNIQUE, class VARCHAR(10), age INT, gender VARCHAR(10),
                    math INT, english INT, science INT, computer INT, social_science INT, study_time FLOAT
                );
            """)
            conn.commit()
            cur.execute("SELECT * FROM students WHERE email = %s", (email,))
            if cur.fetchone():
                st.warning("⚠️ Email already registered! Try logging in.")
            else:
                cur.execute("""
                    INSERT INTO students (name, password, mobile_number, email, class, age, gender, math, english, science, computer, social_science, study_time) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, hashed_password, mobile_number, email, class_name, age, gender, math, english, science, computer, social_science, study_time))
                conn.commit()
                st.success("🎉 Registered successfully!")
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"❌ Database Error: {e}")

# Dashboard
st.title("📊 Study Plan & Learning Resources")
st.subheader("📌 Study Time Allocation")
study_plan = wsm_allocation(math, english, science, computer, social_science, study_time)
for subject, time in study_plan.items():
    st.write(f"✅ {subject}: *{time} hours*")

st.subheader("📖 Study Material")
pdf_option = st.selectbox("📂 Select a PDF", list(pdf_drive_links.keys()))
st.markdown(f"""
    <iframe src="{get_pdf_viewer_link(pdf_drive_links[pdf_option])}" width="100%" height="600px"></iframe>
""", unsafe_allow_html=True)

# Quiz
st.title("📝 Quiz Section")
quiz_questions = {"What is the capital of France?": ["Paris", "London", "Berlin", "Madrid"],
                  "What is 5 + 3?": ["6", "7", "8", "9"],
                  "Which planet is the Red Planet?": ["Earth", "Mars", "Jupiter", "Venus"]}
answers = {"What is the capital of France?": "Paris", "What is 5 + 3?": "8", "Which planet is the Red Planet?": "Mars"}
score = 0
for question, options in quiz_questions.items():
    if st.radio(question, options, index=None) == answers[question]:
        score += 1
if st.button("Submit Quiz"):
    st.success(f"🎉 Your Score: {score}/{len(quiz_questions)}")

if st.button("💡 Generate Advanced Quiz"):
    for q in get_advanced_quiz():
        st.write(q)
