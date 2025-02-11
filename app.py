import streamlit as st
import psycopg2

# Database connection URL
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# Function to connect to the database
def get_db_connection():
    return psycopg2.connect(DB_URL)

st.title("📚 Student Registration/Login Page")

# Streamlit Form for User Registration/Login
with st.form("login_form"):
    name = st.text_input("👤 Name")
    password = st.text_input("🔑 Password", type="password")
    mobile_number = st.text_input("📱 Mobile Number")
    email = st.text_input("📧 Email")

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
                # Insert new user into NeonDB
                cur.execute(
                    "INSERT INTO students (name, password, mobile_number, email) VALUES (%s, %s, %s, %s)",
                    (name, password, mobile_number, email)
                )
                conn.commit()
                st.success("🎉 Registered successfully!")

            # Close the database connection
            cur.close()
            conn.close()
        except Exception as e:
            st.error(f"❌ Error: {e}")
