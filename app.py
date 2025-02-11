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

# Streamlit Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Register", "Dashboard"])

if page == "Register":
    st.title("📚 Student Registration")

    # Registration Form
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
                    st.warning("⚠️ Email already registered! Try logging in.")
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
            st.write(f"✅ {subject}: *{time} hours*")
        
        # Score Summary
        st.subheader("📈 Performance Overview")
        scores = {
            "Math": user_data["math"], "English": user_data["english"],
            "Science": user_data["science"], "Computer": user_data["computer"],
            "Social Science": user_data["social_science"]
        }
        st.bar_chart(scores)

        st.success("📢 Keep up the good work!")
    else:
        st.warning("⚠️ No student data found. Please register first.")


# Function to generate an embeddable Google Drive link
def get_pdf_viewer_link(file_id):
    return f"https://drive.google.com/file/d/{file_id}/preview"

# Google Drive PDF file IDs
pdf_drive_links = {
    "10th_Computer": "1w_hxNste3rVEzx_MwABkY3zbMfwx5qfp",
    "10th_Mathematics": "1g83nbaDLFtUYBW46uWqZSxF6kKGCnoEk",
    "10th_Science": "1Z5Lh-v0lzHZ6tc-SZFZGJQsbykeCW57P",
    "10th_English": "1qYkk7srJSnfzSQahhdcSGFbZ48uptr_d",
    "10th_Social Science": "1fqQlgUs6f8V4CMEEkFxM6lDLHi3FePpq"
}

# Sidebar for PDF Selection
st.sidebar.title("📂 Study Materials")
st.sidebar.write("Click a button to open a PDF:")

selected_pdf = None
for subject, file_id in pdf_drive_links.items():
    if st.sidebar.button(f"📖 {subject}"):
        selected_pdf = get_pdf_viewer_link(file_id)

# Main Page: Display PDF Viewer if a PDF is selected
st.title("📄 PDF Viewer")
if selected_pdf:
    st.markdown(f"""
        <iframe src="{selected_pdf}" width="100%" height="600px"></iframe>
    """, unsafe_allow_html=True)
else:
    st.write("📌 Select a PDF from the sidebar to view it here.")

