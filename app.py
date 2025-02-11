import streamlit as st
import psycopg2
import numpy as np

# Database connection URL
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(DB_URL)

# Function to allocate study time using Weighted Score Method (WSM)
def wsm_allocation(math, eng, sci, comp, soc, total_study_time):
    total_score = math + eng + sci + comp + soc
    weights = [(100 - math) / total_score, (100 - eng) / total_score, 
               (100 - sci) / total_score, (100 - comp) / total_score,
               (100 - soc) / total_score]
    study_times = np.array(weights) * total_study_time
    return {
        "Math": round(study_times[0], 2),
        "English": round(study_times[1], 2),
        "Science": round(study_times[2], 2),
        "Computer": round(study_times[3], 2),
        "Social Science": round(study_times[4], 2)
    }

st.title("📚 Student Registration/Login Page")

# Streamlit Form for User Registration/Login
with st.form("login_form"):
    name = st.text_input("👤 Name")
    password = st.text_input("🔑 Password", type="password")
    mobile_number = st.text_input("📱 Mobile Number")
    email = st.text_input("📧 Email")
    
    class_selection = st.selectbox("📚 Select Class", ["10th", "9th"])
    age = st.number_input("📅 Age", min_value=5, max_value=100, step=1)
    gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])

    st.subheader("🎯 Enter Your Subject Scores (%)")
    math = st.slider("🧮 Math", 0, 100, 50)
    eng = st.slider("📖 English", 0, 100, 50)
    sci = st.slider("🔬 Science", 0, 100, 50)
    comp = st.slider("💻 Computer", 0, 100, 50)
    soc = st.slider("🌍 Social Science", 0, 100, 50)
    study_time = st.number_input("⏳ Daily Study Time (hours)", min_value=1.0, max_value=10.0, step=0.5)

    submitted = st.form_submit_button("🚀 Register/Login")

if submitted:
    # Validate inputs
    if not name or not password or not mobile_number or not email:
        st.error("⚠️ Please fill in all fields.")
    else:
        try:
            # Connect to NeonDB
            conn = get_db_connection()
            cur = conn.cursor()

            # Check if the user already exists
            cur.execute("SELECT * FROM students WHERE email=%s", (email,))
            existing_user = cur.fetchone()

            if existing_user:
                st.success("✅ User exists, logged in successfully!")
            else:
                # Insert new user data into NeonDB
                cur.execute("""
                    INSERT INTO students (name, password, mobile_number, email, class, age, gender, math, english, science, computer, social_science, study_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (name, password, mobile_number, email, class_selection, age, gender, math, eng, sci, comp, soc, study_time))
                
                conn.commit()
                st.success("🎉 Registered successfully!")

            # Close the database connection
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"❌ Error: {e}")
