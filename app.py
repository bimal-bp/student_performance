def student_info():
    st.title("Learn Mate - Student Performance Application")
    st.header("Student Information")

    # Student Information
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email")
    mobile_number = st.text_input("Mobile Number")

    # Branch-wise subject selection
    st.subheader("Select Your Branch")
    branch = st.selectbox(
        "Choose your branch",
        options=[
            "Computer Science",
            "Artificial Intelligence",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Civil Engineering"
        ],
        key="branch"
    )

    # Common subjects for all branches
    common_subjects = [
        "Engineering Mathematics", "Engineering Physics", "Engineering Chemistry",
        "Basic Electrical and Electronical Engineering", "Web Technologies", "Programming",
        "Data Structures & Algorithms", "Operating Systems", "Computer Networks",
        "Cryptography & Network Security", "Big Data Technologies", "Cloud Computing",
        "Cyber Security", "Blockchain Technology", "IoT (Internet of Things)",
        "Introduction to AI & ML", "Data Science & Analytics", "Probability & Statistics",
        "Engineering Drawing", "Engineering Economics & Financial Management"
    ]

    # Branch-specific subjects
    branch_subjects = {
        "Computer Science": [
            "Advanced Programming", "Database Management Systems", "Software Engineering",
            "Machine Learning", "Artificial Intelligence", "Computer Architecture"
        ],
        "Artificial Intelligence": [
            "Deep Learning", "Natural Language Processing", "Computer Vision",
            "Reinforcement Learning", "AI Ethics", "Robotics"
        ],
        "Electrical Engineering": [
            "Circuit Theory", "Power Systems", "Control Systems",
            "Signal Processing", "Microelectronics", "Renewable Energy Systems"
        ],
        "Mechanical Engineering": [
            "Thermodynamics", "Fluid Mechanics", "Solid Mechanics",
            "Manufacturing Processes", "Heat Transfer", "Machine Design"
        ],
        "Civil Engineering": [
            "Structural Analysis", "Geotechnical Engineering", "Transportation Engineering",
            "Environmental Engineering", "Construction Management", "Hydrology"
        ]
    }

    # Combine common and branch-specific subjects
    all_subjects = common_subjects + branch_subjects.get(branch, [])

    # Display all subjects in a dropdown
    st.subheader("Select Your Subjects")
    selected_subjects = st.multiselect(
        "Choose your subjects (select up to 10)",
        options=all_subjects,
        default=all_subjects[:10],  # Default to first 10 subjects
        key="subjects"
    )

    # Efficiency levels
    st.subheader("Efficiency Levels")
    col1, col2 = st.columns(2)

    with col1:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"])
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"])

    with col2:
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"])
        conceptual_understanding = st.selectbox("Conceptual Understanding", ["low", "intermediate", "high"])
        time_management = st.selectbox("Time Management", ["low", "intermediate", "high"])

    # Total study time
    study_time = st.number_input("Total Study Time Per Week (hours)", min_value=1, max_value=168)

    if st.button("Save Information"):
        if not email:
            st.error("Please enter an email.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                subjects_str = ", ".join(selected_subjects)  # Save selected subjects
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, 
                        problem_solving_efficiency, conceptual_understanding, time_management, selected_subjects, study_time_per_week, branch)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET 
                        name = EXCLUDED.name,
                        age = EXCLUDED.age, 
                        mobile_number = EXCLUDED.mobile_number,
                        coding_efficiency = EXCLUDED.coding_efficiency,
                        math_efficiency = EXCLUDED.math_efficiency,
                        problem_solving_efficiency = EXCLUDED.problem_solving_efficiency,
                        conceptual_understanding = EXCLUDED.conceptual_understanding,
                        time_management = EXCLUDED.time_management,
                        selected_subjects = EXCLUDED.selected_subjects,
                        study_time_per_week = EXCLUDED.study_time_per_week,
                        branch = EXCLUDED.branch
                    """),
                    (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, conceptual_understanding, time_management, subjects_str, study_time, branch)
                )
                conn.commit()
                st.success("✅ Student information saved successfully!")
                st.session_state["email"] = email
                st.session_state["page"] = "Dashboard"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cur.close()
                conn.close()
