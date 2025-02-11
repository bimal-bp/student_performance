import streamlit as st
import psycopg2

# Database connection URL
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

def fetch_quiz_questions():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM quiz_questions;")
        questions = cur.fetchall()
        cur.close()
        conn.close()
        return questions
    except Exception as e:
        st.error(f"❌ Database Error: {e}")
        return []

# Initialize session state for user data and quiz state
if "user_data" not in st.session_state:
    st.session_state["user_data"] = {"name": "John Doe"}  # Example user data

if "quiz_started" not in st.session_state:
    st.session_state["quiz_started"] = False

if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = []

if "score" not in st.session_state:
    st.session_state["score"] = 0

# Display the dashboard
user_data = st.session_state["user_data"]
st.title("📊 Student Dashboard")
st.subheader(f"Welcome, {user_data['name']}!")

# Start the quiz session
if not st.session_state["quiz_started"]:
    if st.button("📝 Start Quiz Session"):
        st.session_state["quiz_started"] = True
        st.session_state["user_answers"] = []  # Reset answers
        st.session_state["score"] = 0  # Reset score

# If the quiz is started, display questions
if st.session_state["quiz_started"]:
    questions = fetch_quiz_questions()
    if questions:
        for i, (question, opt_a, opt_b, opt_c, opt_d, correct) in enumerate(questions):
            st.write(f"**Q{i+1}: {question}**")
            # Use a unique key for each radio button
            selected_option = st.radio(
                "Select an answer:",
                [opt_a, opt_b, opt_c, opt_d],
                key=f"q{i}"
            )
            # Store the user's answer in session state
            if i >= len(st.session_state["user_answers"]):
                st.session_state["user_answers"].append(selected_option)
            else:
                st.session_state["user_answers"][i] = selected_option

        # Submit button to calculate the score
        if st.button("Submit Answers"):
            st.session_state["score"] = 0
            for i, (_, _, _, _, correct) in enumerate(questions):
                if st.session_state["user_answers"][i] == correct:
                    st.session_state["score"] += 1
            st.success(f"✅ Your Score: {st.session_state['score']}/{len(questions)}")
            st.session_state["quiz_started"] = False  # End the quiz
    else:
        st.warning("⚠️ No quiz questions available.")
