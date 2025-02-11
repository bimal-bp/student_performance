import streamlit as st
import psycopg2
import hashlib

# Database connection URL
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(DB_URL)

# Function to hash passwords securely
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

st.title("📚 Student Registration Page")

# Streamlit Form for User Registration
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
    # Validate inputs
    if not name or not password or not mobile_number or not email:
        st.error("⚠️ Please fill in all required fields (Name, Password, Mobile Number, Email).")
    else:
        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # Hash the password before storing
            hashed_password = hash_password(password)

            # Ensure the table exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    mobile_number VARCHAR(20) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    class VARCHAR(10),
                    age INT,
                    gender VARCHAR(10),
                    math INT,
                    english INT,
                    science INT,
                    computer INT,
                    social_science INT,
                    study_time FLOAT
                );
            """)
            conn.commit()

            # Check if the email already exists
            cur.execute("SELECT * FROM students WHERE email = %s", (email,))
            existing_user = cur.fetchone()

            if existing_user:
                st.warning("⚠️ Email already registered! Try logging in.")
            else:
                # Insert new student data
                cur.execute("""
                    INSERT INTO students 
                    (name, password, mobile_number, email, class, age, gender, math, english, science, computer, social_science, study_time) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, hashed_password, mobile_number, email, class_name, age, gender, math, english, science, computer, social_science, study_time))

                conn.commit()
                st.success("🎉 Registered successfully!")

            # Close the database connection
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"❌ Database Error: {e}")
