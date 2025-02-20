import streamlit as st
import psycopg2

# Database Connection (NeonDB)
DB_URL = "postgresql://neondb_owner:npg_hnkGvx5eFaf0@ep-crimson-bread-a136p4y6-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

# Create users table if not exists
conn = get_db_connection()
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY, 
        name TEXT, 
        email TEXT UNIQUE, 
        password TEXT
    )
''')
conn.commit()
conn.close()

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_email = None

# Function to register a new user
def register_user(name, email, password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        st.success("Registration successful! You can now log in.")
    except psycopg2.IntegrityError:
        st.error("Email already registered. Try logging in.")
    finally:
        c.close()
        conn.close()

# Function to validate user login
def login_user(email, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
    user = c.fetchone()
    c.close()
    conn.close()
    if user:
        st.session_state.authenticated = True
        st.session_state.user_email = email
        st.session_state.user_name = user[1]
        st.success(f"Welcome, {user[1]}! 🎉")
    else:
        st.error("Invalid email or password. Please try again.")

# Function to update user profile
def update_profile(new_name, new_password):
    if st.session_state.authenticated:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET name = %s, password = %s WHERE email = %s", (new_name, new_password, st.session_state.user_email))
        conn.commit()
        c.close()
        conn.close()
        st.session_state.user_name = new_name
        st.success("Profile updated successfully!")

# Function to logout
def logout():
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_name = None
    st.success("You have been logged out.")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
menu = st.sidebar.radio("Select an option:", ["Home", "Login", "Register", "Dashboard", "Update Profile", "Logout"])

# Home Page
if menu == "Home":
    st.title("📚 Study Dashboard")
    st.write("Welcome to the study dashboard. Register or log in to access your personalized study plan.")

# Registration Page
elif menu == "Register":
    st.title("📝 Register")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if name and email and password:
            register_user(name, email, password)
        else:
            st.warning("Please fill all fields.")

# Login Page
elif menu == "Login":
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email and password:
            login_user(email, password)
        else:
            st.warning("Please enter email and password.")

# Dashboard Page (Only for logged-in users)
elif menu == "Dashboard":
    if st.session_state.authenticated:
        st.title(f"📌 Welcome, {st.session_state.user_name}!")
        st.subheader("Your Study Plan 📖")
        st.write("📝 Personalized study plan coming soon...")
    else:
        st.warning("Please log in to access the dashboard.")

# Update Profile Page
elif menu == "Update Profile":
    if st.session_state.authenticated:
        st.title("🔧 Update Profile")
        new_name = st.text_input("New Name", st.session_state.user_name)
        new_password = st.text_input("New Password", type="password")
        if st.button("Update"):
            if new_name and new_password:
                update_profile(new_name, new_password)
            else:
                st.warning("Please enter all fields.")
    else:
        st.warning("Please log in to update your profile.")

# Logout Page
elif menu == "Logout":
    logout()
