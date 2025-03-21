import streamlit as st
import psycopg2
from psycopg2 import sql
import numpy as np
import pickle
import random
import hashlib

# Database Connection Strings
AUTH_DB_URL = "postgresql://neondb_owner:npg_P0wyolC1KBLW@ep-holy-mud-a5su2ghw-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
APP_DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_auth_db_connection():
    return psycopg2.connect(AUTH_DB_URL)

def get_app_db_connection():
    return psycopg2.connect(APP_DB_URL)

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Sign-Up Page
def sign_up():
    st.title("Sign Up")
    st.write("Create a new account to access the application.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password != confirm_password:
            st.error("Passwords do not match.")
        else:
            conn = get_auth_db_connection()
            cur = conn.cursor()
            try:
                hashed_password = hash_password(password)
                cur.execute(
                    sql.SQL("""
                        INSERT INTO users (email, password)
                        VALUES (%s, %s)
                        ON CONFLICT (email) DO NOTHING
                    """),
                    (email, hashed_password)
                )
                conn.commit()
                st.success("✅ Account created successfully! Please log in.")
                # Set a flag in session state to indicate successful sign-up
                st.session_state["signup_success"] = True
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cur.close()
                conn.close()

    # Check if sign-up was successful and show the "Go to Login" button
    if st.session_state.get("signup_success", False):
        if st.button("Go to Login"):
            st.session_state["page"] = "Login"
            # Clear the signup success flag
            del st.session_state["signup_success"]
            st.rerun()

# Login Page
def login():
    st.title("Login")
    st.write("Log in to access the application.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_auth_db_connection()
        cur = conn.cursor()
        try:
            hashed_password = hash_password(password)
            cur.execute(
                "SELECT email FROM users WHERE email = %s AND password = %s",
                (email, hashed_password)
            )
            user = cur.fetchone()
            if user:
                st.success("✅ Login successful!")
                st.session_state["email"] = email
                st.session_state["page"] = "Student Info"
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cur.close()
            conn.close() 

# Student Info Page (Placeholder)
def student_info():
    st.title("Student Info")
    st.write("This is the student info page.")
    # Add your student info form here
    if st.button("Go to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

# Allocate Study Time (Placeholder)
def allocate_study_time(selected_subjects, study_time, coding_eff, problem_solving_eff):
    # Placeholder logic for allocating study time
    allocation = {}
    for subject in selected_subjects:
        allocation[subject] = study_time // len(selected_subjects)
    return allocation

# Dashboard Page
def dashboard():
    st.header("Student Dashboard")

    if "email" not in st.session_state:
        st.warning("Please log in to view your dashboard.")
        return

    email = st.session_state["email"]
    try:
        conn = get_app_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week, branch FROM students WHERE email = %s",
            (email,),
        )
        student = cur.fetchone()
        cur.close()
        conn.close()

        if student:
            col1, col2 = st.columns(2)
            with col1:
                st.write("### Student Information")
                st.write(f"**Name:** {student[0]}")
                st.write(f"**Age:** {student[1]}")
                st.write(f"**Email:** {student[2]}")
                st.write(f"**Mobile Number:** {student[3]}")
                st.write(f"**Study Time Per Week:** {student[8]} h/w")
                st.write(f"**Branch:** {student[9]}")

            with col2:
                st.write("### Study Time Allocation")
                selected_subjects = student[7].split(", ")
                study_time = student[8]
                coding_eff = student[4]
                problem_solving_eff = student[6]
                study_allocation = allocate_study_time(selected_subjects, study_time, coding_eff, problem_solving_eff)
                for subject, hours in study_allocation.items():
                    st.write(f"- **{subject}:** {hours} h/w")

            st.markdown("---")
            col3, col4, col5 = st.columns(3)
            with col3:
                if st.button("Predict Future Score 🎯"):
                    st.session_state["page"] = "Predict Future Score"
                    st.rerun()
            with col4:
                if st.button("Take a Quiz 📝"):
                    st.session_state["page"] = "Quiz"
                    st.rerun()
            with col5:
                if st.button("Study Content 📚"):
                    st.session_state["page"] = "Study Content"
                    st.rerun()
        else:
            st.warning("No records found for the logged-in user.")
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

# Landing Page
def landing_page():
    st.title("Welcome to Learn Mate")
    st.write("Please choose an option to get started.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign Up"):
            st.session_state["page"] = "Sign Up"
            st.rerun()
    with col2:
        if st.button("Login"):
            st.session_state["page"] = "Login"
            st.rerun()

# Main Function
def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Landing Page"

    if st.session_state["page"] == "Landing Page":
        landing_page()
    elif st.session_state["page"] == "Sign Up":
        sign_up()
    elif st.session_state["page"] == "Login":
        login()
    elif st.session_state["page"] == "Student Info":
        student_info()
    elif st.session_state["page"] == "Dashboard":
        dashboard()

if __name__ == "__main__":
    main()
