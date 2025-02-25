import streamlit as st
import pandas as pd
import numpy as np

# Page 1: Login Page
def login_page():
    st.title("Student Login Page")
    st.write("Please enter your details below:")

    # Input fields
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    study_time = st.number_input("Study Time per Week (in hours)", min_value=1, max_value=168)

    # Dropdown for selecting 10 subjects
    subjects = [
        "Data Structures and Algorithms", "Operating Systems", "Database Management Systems",
        "Computer Networks", "Software Engineering", "Python", "Object-Oriented Programming",
        "Web Technologies", "Theory of Computation", "Compiler Design", "Artificial Intelligence",
        "Machine Learning", "Cloud Computing", "Cybersecurity", "Distributed Systems",
        "Deep Learning", "Data Mining", "Big Data Analytics", "Natural Language Processing",
        "Reinforcement Learning", "Data Visualization", "Business Intelligence", "Neural Networks",
        "Computer Vision", "Pattern Recognition", "Business Strategy and Analytics",
        "Financial and Management Accounting", "Business Process Management", "Enterprise Systems",
        "Structural Analysis", "Fluid Mechanics", "Engineering Mechanics", "Geotechnical Engineering",
        "Construction Materials and Techniques", "Surveying", "Reinforced Concrete Structures",
        "Steel Structures", "Transportation Engineering", "Environmental Engineering",
        "Hydrology and Water Resources Engineering", "Foundation Engineering"
    ]
    selected_subjects = st.multiselect("Select 10 Subjects", subjects, max_selections=10)

    if st.button("Submit"):
        if len(selected_subjects) != 10:
            st.error("Please select exactly 10 subjects.")
        else:
            # Store student info in session state
            st.session_state.student_info = {
                "Name": name,
                "Age": age,
                "Gender": gender,
                "Phone": phone,
                "Email": email,
                "Study Time": study_time,
                "Selected Subjects": selected_subjects
            }
            st.session_state.page = "dashboard"
            st.experimental_rerun()

# Page 2: Dashboard
def dashboard_page():
    st.title("Student Dashboard")

    # Box 1: Student Info
    st.subheader("Student Information")
    student_info = st.session_state.student_info
    st.write(f"Name: {student_info['Name']}")
    st.write(f"Age: {student_info['Age']}")
    st.write(f"Gender: {student_info['Gender']}")
    st.write(f"Phone: {student_info['Phone']}")
    st.write(f"Email: {student_info['Email']}")
    st.write(f"Study Time per Week: {student_info['Study Time']} hours")
    st.write("Selected Subjects:")
    for subject in student_info["Selected Subjects"]:
        st.write(f"- {subject}")

    # Box 2: MCDM-based Time Allocation
    st.subheader("Time Allocation for Subjects")
    study_time = student_info["Study Time"]
    subjects = student_info["Selected Subjects"]
    weights = np.random.dirichlet(np.ones(len(subjects)), size=1)[0]  # Random weights for MCDM
    time_allocation = (weights * study_time).round(2)

    time_df = pd.DataFrame({
        "Subject": subjects,
        "Allocated Time (hours)": time_allocation
    })
    st.dataframe(time_df)

    # Box 3: Content
    st.subheader("Study Content")
    selected_subject = st.selectbox("Select a Subject to Study", subjects)
    st.write(f"Here is some content for {selected_subject}:")
    st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")

    # Buttons for Predict and Quiz
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Predict Your Future Score"):
            st.write("Prediction feature will be implemented here.")
    with col2:
        if st.button("Quiz Section"):
            st.session_state.page = "quiz"
            st.experimental_rerun()

# Page 3: Quiz
def quiz_page():
    st.title("Quiz Section")
    st.write("Quiz feature will be implemented here.")

    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.experimental_rerun()

# Main App Logic
def main():
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "dashboard":
        dashboard_page()
    elif st.session_state.page == "quiz":
        quiz_page()

if __name__ == "__main__":
    main()
