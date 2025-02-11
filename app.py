import streamlit as st
import psycopg2
import hashlib
import numpy as np

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

if "user_data" in st.session_state:
    user_data = st.session_state["user_data"]
    st.title("📊 Student Dashboard")
    st.subheader(f"Welcome, {user_data['name']}!")

    # Button for Quiz Session
    if st.button("📝 Start Quiz Session"):
        questions = fetch_quiz_questions()
        if questions:
            score = 0
            for i, (question, opt_a, opt_b, opt_c, opt_d, correct) in enumerate(questions):
                st.write(f"**Q{i+1}: {question}**")
                selected_option = st.radio("Select an answer:", [opt_a, opt_b, opt_c, opt_d], key=f"q{i}")
                if selected_option == correct:
                    score += 1
            st.success(f"✅ Your Score: {score}/{len(questions)}")
        else:
            st.warning("⚠️ No quiz questions available.")
