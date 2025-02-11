import psycopg2

DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

try:
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    db_version = cur.fetchone()
    print(f"Connected to database: {db_version[0]}")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")
import streamlit as st
import psycopg2

DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

st.title("📚 Student Login Page")

with st.form("login_form"):
    name = st.text_input("👤 Name")
    password = st.text_input("🔑 Password", type="password")
    mobile_number = st.text_input("📱 Mobile Number")
    email = st.text_input("📧 Email")
    
    submitted = st.form_submit_button("🚀 Register/Login")

if submitted:
    cur.execute("SELECT * FROM students WHERE email=%s", (email,))
    existing_user = cur.fetchone()
    
    if existing_user:
        st.success("✅ User exists, logged in successfully!")
    else:
        cur.execute("INSERT INTO students (name, password, mobile_number, email) VALUES (%s, %s, %s, %s)",
                    (name, password, mobile_number, email))
        conn.commit()
        st.success("🎉 Registered successfully!")
