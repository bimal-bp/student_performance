def login_and_student_info():
    st.title("Student Performance Web Application")
    st.header("Login and Student Information")

    # Use columns to display input fields side by side
    col1, col2 = st.columns(2)

    with col1:
        # Input fields
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        email = st.text_input("Email")
        mobile_number = st.text_input("Mobile Number")

    with col2:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"])
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"])
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"])

    # Subject selection
    subjects = {
        "Computer Science and Engineering (CSE)": {
            "Data Structures and Algorithms": 10,
            "Operating Systems": 9,
            "Database Management Systems (DBMS)": 9,
            "Computer Networks": 8,
            "Software Engineering": 7,
            "Python": 10,
            "Object-Oriented Programming (Java/C/C++)": 10,
            "Web Technologies": 7,
            "Theory of Computation": 8,
            "Compiler Design": 7,
            "Artificial Intelligence": 9,
            "Machine Learning": 9,
            "Cloud Computing": 8,
            "Cybersecurity": 8,
            "Distributed Systems": 7
        },
        "Electrical and Electronics Engineering (EEE)": {
            "Electrical Machines": 10,
            "Power Systems": 9,
            "Control Systems": 9,
            "Electrical Circuit Analysis": 10,
            "Power Electronics": 9,
            "Analog Electronics": 8,
            "Digital Electronics": 8,
            "Electromagnetic Field Theory": 7,
            "Microprocessors and Microcontrollers": 8,
            "Renewable Energy Systems": 7,
            "Electrical Measurements and Instrumentation": 8
        },
        "Electronics and Communication Engineering (ECE)": {
            "Analog and Digital Communication": 10,
            "Signals and Systems": 9,
            "Digital Signal Processing (DSP)": 9,
            "VLSI Design": 9,
            "Microprocessors and Microcontrollers": 8,
            "Electromagnetic Field Theory": 8,
            "Control Systems": 8,
            "Optical Communication": 7,
            "Embedded Systems": 9,
            "Wireless Communication": 9,
            "Antenna and Wave Propagation": 7
        },
        "Civil Engineering": {
            "Structural Analysis": 10,
            "Fluid Mechanics": 9,
            "Engineering Mechanics": 8,
            "Geotechnical Engineering": 9,
            "Construction Materials and Techniques": 8,
            "Surveying": 8,
            "Reinforced Concrete Structures": 10,
            "Steel Structures": 8,
            "Transportation Engineering": 8,
            "Environmental Engineering": 9,
            "Hydrology and Water Resources Engineering": 7,
            "Foundation Engineering": 8
        }
    }

    # Flatten the subjects dictionary into a list of tuples (subject, rating)
    all_subjects = []
    for category, category_subjects in subjects.items():
        for subject, rating in category_subjects.items():
            all_subjects.append((subject, rating))

    # Display subjects in a multiselect dropdown
    selected_subjects = st.multiselect(
        "Select up to 10 subjects",
        options=[f"{subject} – {rating}/10" for subject, rating in all_subjects],
        default=[],
        key="subject_selection"
    )

    # Extract the subject names from the selected options
    selected_subjects = [subject.split(" – ")[0] for subject in selected_subjects]

    # Study time input
    study_time = st.number_input("Study Time Per Week (hours)", min_value=1, max_value=168)

    # Save to database
    if st.button("Save Information"):
        if len(selected_subjects) != 10:
            st.error("Please select exactly 10 subjects.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """),
                    (name, age, email, mobile_number, coding_eff, math_eff, problem_solving_eff, selected_subjects, study_time)
                )
                conn.commit()
                st.success("Student information saved successfully!")
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                cur.close()
                conn.close()
