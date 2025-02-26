import streamlit as st
import pandas as pd
import psycopg2
import google.generativeai as genai

# Gemini API Setup
genai.configure(api_key="AIzaSyCNV_-fekzYdly2JoVBZ8wa-k3J-ZMbLbs")

# Database connection
DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

# Function to create table if it doesn't exist
def create_table():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name TEXT,
            age INTEGER,
            gender TEXT,
            phone TEXT UNIQUE,
            email TEXT UNIQUE,
            coding TEXT,
            mathematics TEXT,
            problem_solving TEXT,
            study_time INTEGER,
            subjects TEXT[]
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Function to insert student data
def insert_student(name, age, gender, phone, email, coding, math, problem_solving, study_time, subjects):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO students (name, age, gender, phone, email, coding, mathematics, problem_solving, study_time, subjects)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (phone, email) DO NOTHING
    """, (name, age, gender, phone, email, coding, math, problem_solving, study_time, subjects))
    conn.commit()
    cur.close()
    conn.close()

# Function to fetch student data
def fetch_student(phone):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE phone = %s", (phone,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    return student

# Function to generate AI-based quiz using Gemini API
def generate_quiz(question):
    response = genai.chat(prompt=f"Create a multiple-choice quiz question with 4 options for {question}. Provide the correct answer.")
    return response.text

# Create the table initially
create_table()

# Session Management
if "page" not in st.session_state:
    st.session_state["page"] = "login"

if st.session_state["page"] == "login":
    st.title("Student Login")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=5, max_value=100, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")

    st.write("### Select Your Proficiencies")
    coding = st.selectbox("Coding Proficiency", ["Beginner", "Intermediate", "Expert"])
    mathematics = st.selectbox("Mathematics Proficiency", ["Beginner", "Intermediate", "Expert"])
    problem_solving = st.selectbox("Problem Solving Proficiency", ["Beginner", "Intermediate", "Expert"])
    study_time = st.slider("Study Time per Week (hrs)", 0, 50, 10)

    subjects = [
        "Data Structures", "Operating Systems", "DBMS", "Computer Networks",
        "Software Engineering", "Python", "OOP (Java/C/C++)", "Web Tech",
        "Theory of Computation", "Compiler Design", "AI", "ML", "Cloud Computing",
        "Cybersecurity", "Distributed Systems", "Deep Learning", "Data Mining",
        "Big Data", "NLP", "Reinforcement Learning", "Data Visualization", "Business Intelligence"
    ]
    selected_subjects = st.multiselect("Select 10 Subjects", subjects, max_selections=10)

    if st.button("Save Details"):
        existing_student = fetch_student(phone)
        if existing_student:
            insert_student(name, age, gender, phone, email, coding, mathematics, problem_solving, study_time, selected_subjects)
            st.success("Student data updated successfully!")
        else:
            insert_student(name, age, gender, phone, email, coding, mathematics, problem_solving, study_time, selected_subjects)
            st.success("Student data saved successfully!")

    if st.button("Go to Dashboard") and phone:
        st.session_state["student_phone"] = phone
        st.session_state["page"] = "dashboard"

elif st.session_state["page"] == "dashboard":
    st.title("📊 Student Dashboard")
    phone = st.session_state.get("student_phone", "")

    student_info = fetch_student(phone)
    if student_info:
        _, name, age, gender, phone, email, coding, mathematics, problem_solving, study_time, subjects = student_info
        subjects = ", ".join(subjects)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Student Info")
            st.write(f"**Name:** {name}")
            st.write(f"**Age:** {age}")
            st.write(f"**Gender:** {gender}")
            st.write(f"**Email:** {email}")
            st.write(f"**Contact Number:** {phone}")
            st.write(f"**Weekly Study Time:** {study_time} hrs")
            st.write(f"**Coding Proficiency:** {coding}")
            st.write(f"**Mathematics Proficiency:** {mathematics}")
            st.write(f"**Problem Solving Proficiency:** {problem_solving}")

        with col2:
            st.subheader("📚 Subjects Selected")
            for subject in subjects.split(", "):
                if st.button(subject):
                    st.write(f"**{subject} Content:**")
                    st.write(f"Here is some study material for {subject}.")
    
    st.subheader("📝 Quiz Section")
    st.write("Test your knowledge with some quizzes!")

    quiz_questions = [
        {"question": "What is the time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"], "answer": "O(log n)"},
        {"question": "Which SQL command is used to retrieve data?", "options": ["INSERT", "UPDATE", "SELECT", "DELETE"], "answer": "SELECT"},
        {"question": "What does HTTP stand for?", "options": ["Hypertext Transfer Protocol", "Hyper Transfer Process", "High Tech Protocol", "Hyper Transfer Path"], "answer": "Hypertext Transfer Protocol"},
        {"question": "Which language is primarily used for Machine Learning?", "options": ["Java", "C++", "Python", "Ruby"], "answer": "Python"},
        {"question": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Linked List", "Tree"], "answer": "Stack"}
    ]

    for q in quiz_questions:
        st.write(f"**{q['question']}**")
        user_answer = st.radio("", q["options"], key=q["question"])
        if user_answer == q["answer"]:
            st.success("✅ Correct!")
        elif user_answer:
            st.error("❌ Wrong answer!")

    st.subheader("🔍 AI Quiz (Powered by Gemini)")
    topic = st.text_input("Enter a topic for a quiz question:")
    if st.button("Generate AI Quiz"):
        ai_quiz = generate_quiz(topic)
        st.write(ai_quiz)

    if st.button("Back to Login"):
        st.session_state["page"] = "login"
