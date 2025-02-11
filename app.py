import streamlit as st
import psycopg2
import hashlib
import numpy as np

# Database connection URL
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def wsm_allocation(math, eng, sci, comp, soc, total_study_time):
    total_score = math + eng + sci + comp + soc
    if total_score == 0:
        return {"Math": 0, "English": 0, "Science": 0, "Computer": 0, "Social Science": 0}
    weights = [(100 - math) / total_score, (100 - eng) / total_score, 
               (100 - sci) / total_score, (100 - comp) / total_score,
               (100 - soc) / total_score]
    study_times = np.array(weights) * total_study_time
    return {"Math": round(study_times[0], 2), "English": round(study_times[1], 2),
            "Science": round(study_times[2], 2), "Computer": round(study_times[3], 2),
            "Social Science": round(study_times[4], 2)}

def fetch_quiz_questions():
    """Fetch quiz questions from the database."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM quiz_questions;")
        questions = cur.fetchall()
        cur.close()
        return questions
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Streamlit Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Register", "Dashboard"])

if page == "Register":
    st.title("\U0001F4DA Student Registration")

    # Registration Form
    with st.form("registration_form"):
        name = st.text_input("\U0001F464 Name", max_chars=100)
        password = st.text_input("\U0001F511 Password", type="password", max_chars=255)
        mobile_number = st.text_input("\U0001F4F1 Mobile Number", max_chars=20)
        email = st.text_input("\U0001F4E7 Email", max_chars=100)
        class_name = st.text_input("\U0001F3EB Class", max_chars=10)
        age = st.number_input("\U0001F382 Age", min_value=1, max_value=100, step=1)
        gender = st.selectbox("⚧ Gender", ["Male", "Female", "Other"])
        math = st.number_input("\U0001F522 Math Score", min_value=0, max_value=100, step=1)
        english = st.number_input("\U0001F4D6 English Score", min_value=0, max_value=100, step=1)
        science = st.number_input("\U0001F52C Science Score", min_value=0, max_value=100, step=1)
        computer = st.number_input("\U0001F4BB Computer Score", min_value=0, max_value=100, step=1)
        social_science = st.number_input("\U0001F30D Social Science Score", min_value=0, max_value=100, step=1)
        study_time = st.number_input("⏳ Study Time (hours per day)", min_value=0.0, max_value=24.0, step=0.1)
        submitted = st.form_submit_button("\U0001F680 Register")

    if submitted:
        if not name or not password or not mobile_number or not email:
            st.error("⚠ Please fill in all required fields.")
        else:
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                hashed_password = hash_password(password)

                # Create Table if not Exists
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100), password VARCHAR(255), mobile_number VARCHAR(20),
                        email VARCHAR(100) UNIQUE, class VARCHAR(10), age INT, gender VARCHAR(10),
                        math INT, english INT, science INT, computer INT, social_science INT, study_time FLOAT
                    );
                """)
                conn.commit()

                # Check if Email Exists
                cur.execute("SELECT * FROM students WHERE email = %s", (email,))
                if cur.fetchone():
                    st.warning("⚠ Email already registered! Try logging in.")
                else:
                    # Insert Student Data
                    cur.execute("""
                        INSERT INTO students (name, password, mobile_number, email, class, age, gender, math, english, science, computer, social_science, study_time) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (name, hashed_password, mobile_number, email, class_name, age, gender, math, english, science, computer, social_science, study_time))
                    conn.commit()

                    # Store Data for Dashboard
                    st.session_state["user_data"] = {
                        "name": name, "math": math, "english": english,
                        "science": science, "computer": computer, "social_science": social_science, "study_time": study_time
                    }
                    st.success("🎉 Registered successfully! Go to the Dashboard to view study plan.")

                cur.close()
                conn.close()
            except Exception as e:
                st.error(f"❌ Database Error: {e}")

elif page == "Dashboard":
    st.title("📊 Student Dashboard")

    if "user_data" in st.session_state:
        user_data = st.session_state["user_data"]
        st.subheader(f"Welcome, {user_data['name']}!")

        # Study Plan Calculation
        study_plan = wsm_allocation(user_data["math"], user_data["english"], user_data["science"],
                                    user_data["computer"], user_data["social_science"], user_data["study_time"])
        st.subheader("📌 Study Time Allocation")
        for subject, time in study_plan.items():
            st.write(f"✅ {subject}: {time} hours")

        # PDF Selection Dropdown
        st.subheader("📂 Study Materials")
        pdf_drive_links = {
            "10th_Computer": "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp",
            "10th_Mathematics": "1g83nbaDLFtUYBW46uWqZSxF6kKGCnoEk",
            "10th_Science": "1Z5Lh-v0lzHZ6tc-SZFZGJQsbykeCW57P",
            "10th_English": "1qYkk7srJSnfzSQahhdcSGFbZ48uptr_d",
            "10th_Social Science": "1fqQlgUs6f8V4CMEEkFxM6lDLHi3FePpq"
        }
        selected_pdf = st.selectbox("Select a subject", list(pdf_drive_links.keys()))
        if selected_pdf:
            st.markdown(f"<iframe src='https://drive.google.com/file/d/{pdf_drive_links[selected_pdf]}/preview' width='100%' height='600px'></iframe>", unsafe_allow_html=True)

        # Quiz Section
        st.subheader("📝 Quiz Section")

        # Initialize session state variables for the quiz
        if "quiz_started" not in st.session_state:
            st.session_state["quiz_started"] = False

        if "user_answers" not in st.session_state:
            st.session_state["user_answers"] = {}

        if "score" not in st.session_state:
            st.session_state["score"] = 0

        # Start the quiz
        if not st.session_state["quiz_started"]:
            if st.button("📝 Start Quiz Session"):
                st.session_state["quiz_started"] = True
                st.session_state["user_answers"] = {}  # Reset previous answers
                st.session_state["score"] = 0  # Reset score

        # If the quiz is started, fetch and display questions
        if st.session_state["quiz_started"]:
            questions = fetch_quiz_questions()
            
            if questions:
                for i, (question, opt_a, opt_b, opt_c, opt_d, correct) in enumerate(questions):
                    st.write(f"**Q{i+1}: {question}**")
                    
                    # Ensure default value in session state
                    if i not in st.session_state["user_answers"]:
                        st.session_state["user_answers"][i] = None

                    # Set unique key for each question
                    selected_option = st.radio(
                        f"Select an answer for Q{i+1}:",
                        [opt_a, opt_b, opt_c, opt_d],
                        key=f"q{i}"
                    )

                    # Store user answer safely
                    if selected_option:
                        st.session_state["user_answers"][i] = selected_option

                # Submit button
                if st.button("✅ Submit Answers"):
                    # Ensure session state keys exist before scoring
                    st.session_state["score"] = sum(
                        1 for i, (_, _, _, _, _, correct) in enumerate(questions)
                        if i in st.session_state["user_answers"] and st.session_state["user_answers"][i] == correct
                    )

                    st.success(f"🎯 Your Score: **{st.session_state['score']}/{len(questions)}**")
                    st.session_state["quiz_started"] = False  # End quiz session
            else:
                st.warning("⚠️ No quiz questions available.")
