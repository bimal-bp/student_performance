import streamlit as st
import numpy as np

# Function to allocate study time
def wsm_allocation(math, eng, sci, comp, total_study_time):
    total_score = math + eng + sci + comp
    weights = [(100 - math) / total_score, (100 - eng) / total_score, (100 - sci) / total_score, (100 - comp) / total_score]
    study_times = np.array(weights) * total_study_time
    return {
        "Math": round(study_times[0], 2),
        "English": round(study_times[1], 2),
        "Science": round(study_times[2], 2),
        "Computer": round(study_times[3], 2)
    }

# ✅ Corrected GitHub raw PDF URLs
pdf_urls = {
    "Basics of Computer.pdf": "https://bimal-bp.github.io/student_performance/Basics%20of%20Computer.pdf",
    "Basic Mathematics.pdf": "https://bimal-bp.github.io/student_performance/basic_maths.pdf"
}

# Streamlit UI
st.set_page_config(page_title="Study Time Allocator", layout="wide")

st.title("📚 Study Time Allocator Dashboard")

# Subject Score Inputs
with st.form("user_info"):
    name = st.text_input("👤 Name")
    age = st.number_input("📅 Age", min_value=5, max_value=100, step=1)
    gender = st.selectbox("🚻 Gender", ["Male", "Female", "Other"])
    student_class = st.text_input("🏫 Class")

    st.subheader("🎯 Enter Your Subject Scores (%)")
    math = st.slider("🧮 Math", 0, 100, 50)
    eng = st.slider("📖 English", 0, 100, 50)
    sci = st.slider("🔬 Science", 0, 100, 50)
    comp = st.slider("💻 Computer", 0, 100, 50)
    study_time = st.number_input("⏳ Daily Study Time (hours)", min_value=1.0, max_value=10.0, step=0.5)

    submitted = st.form_submit_button("📊 Generate Study Plan")

if submitted:
    study_plan = wsm_allocation(math, eng, sci, comp, study_time)

    st.subheader("📌 Study Time Allocation")
    for subject, time in study_plan.items():
        st.write(f"✅ {subject}: **{time} hours**")

# 📖 **PDF Viewer**
st.subheader("📄 Read PDF Notes")
pdf_option = st.selectbox("📂 Select a PDF", list(pdf_urls.keys()))

# ✅ **Embed the PDF in Streamlit**
pdf_url = pdf_urls[pdf_option]
pdf_viewer = f"""
    <iframe src="{pdf_url}" width="700" height="600"></iframe>
"""
st.markdown(pdf_viewer, unsafe_allow_html=True)
