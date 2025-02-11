import streamlit as st
import psycopg2

# Database connection URL
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

def fetch_quiz_questions():
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

# Initialize session state
if "user_data" not in st.session_state:
    st.session_state["user_data"] = {"name": "John Doe"}

if "quiz_started" not in st.session_state:
    st.session_state["quiz_started"] = False

if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = []

if "score" not in st.session_state:
    st.session_state["score"] = 0

# Display dashboard
user_data = st.session_state["user_data"]
st.title("📊 Student Dashboard")
st.subheader(f"Welcome, {user_data['name']}!")

# Start the quiz
if not st.session_state["quiz_started"]:
    if st.button("📝 Start Quiz Session"):
        st.session_state["quiz_started"] = True
        st.session_state["user_answers"] = []
        st.session_state["score"] = 0

if st.session_state["quiz_started"]:
    questions = fetch_quiz_questions()
    
    if questions:
        # st.write("Debug: Questions fetched from the database:")
        for q in questions:
           # st.write(f"Debug: {q}")

        for i, question_data in enumerate(questions):
            if len(question_data) == 6:
                question, opt_a, opt_b, opt_c, opt_d, correct = question_data
                st.write(f"**Q{i+1}: {question}**")

                selected_option = st.radio(
                    "Select an answer:",
                    [opt_a, opt_b, opt_c, opt_d],
                    key=f"q{i}"
                )

                if i >= len(st.session_state["user_answers"]):
                    st.session_state["user_answers"].append(selected_option if selected_option else None)
                else:
                    st.session_state["user_answers"][i] = selected_option if selected_option else None
            else:
                st.error(f"❌ Invalid question format: {question_data}")

        if st.button("Submit Answers"):
            st.session_state["score"] = 0
            for i, question_data in enumerate(questions):
                if len(question_data) == 6:
                    _, _, _, _, _, correct = question_data
                    if st.session_state["user_answers"][i] and st.session_state["user_answers"][i] == correct:
                        st.session_state["score"] += 1
            
            st.success(f"✅ Your Score: {st.session_state['score']}/{len(questions)}")
            st.session_state["quiz_started"] = False
    else:
        st.warning("⚠️ No quiz questions available.")
