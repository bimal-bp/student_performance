def student_info():
    st.title("📚 Learn Mate - Student Performance Application")
    st.header("Student Information")

    # Check if the user is logged in (i.e., email is in session)
    email = st.session_state.get("email")

    # Initialize variables to store existing data
    name = ""
    age = 0
    mobile_number = ""
    coding_eff = "intermediate"
    math_eff = "intermediate"
    problem_solving_eff = "intermediate"
    selected_subjects = []
    study_time = 0

    # If the user is logged in, fetch existing data
    if email:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT name, age, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week FROM students WHERE email = %s",
                (email,),
            )
            student = cur.fetchone()
            cur.close()
            conn.close()

            if student:
                name = student[0]
                age = student[1]
                mobile_number = student[2]
                coding_eff = student[3]
                math_eff = student[4]
                problem_solving_eff = student[5]
                selected_subjects = student[6].split(", ") if student[6] else []
                study_time = student[7]
        except Exception as e:
            st.error(f"❌ Error fetching existing data: {e}")

    # Input fields (pre-filled with existing data if available)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", value=name)
        age = st.number_input("Age", min_value=1, max_value=100, value=age)
        email_input = st.text_input("Email", value=email if email else "")
        mobile_number = st.text_input("Mobile Number", value=mobile_number)

    with col2:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"], index=["low", "intermediate", "high"].index(coding_eff))
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"], index=["low", "intermediate", "high"].index(math_eff))
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"], index=["low", "intermediate", "high"].index(problem_solving_eff))

    selected_subjects = st.multiselect("Select up to 10 subjects", options=list(subject_ratings.keys()), default=selected_subjects)
    
    if len(selected_subjects) > 10:
        st.error("⚠ Please select a maximum of 10 subjects.")

    study_time = st.number_input("Total Study Time Per Week (hours)", min_value=1, max_value=168, value=study_time)

    if st.button("Save Information"):
        if len(selected_subjects) > 10:
            st.error("⚠ Please select a maximum of 10 subjects.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                subjects_str = ", ".join(selected_subjects)
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET 
                        name = EXCLUDED.name,
                        age = EXCLUDED.age, 
                        mobile_number = EXCLUDED.mobile_number,
                        coding_efficiency = EXCLUDED.coding_efficiency,
                        math_efficiency = EXCLUDED.math_efficiency,
                        problem_solving_efficiency = EXCLUDED.problem_solving_efficiency,
                        selected_subjects = EXCLUDED.selected_subjects,
                        study_time_per_week = EXCLUDED.study_time_per_week
                    """),
                    (name, age, email_input, mobile_number, coding_eff, math_eff, problem_solving_eff, subjects_str, study_time)
                )
                conn.commit()
                st.success("✅ Student information saved successfully!")

                # Update session state with the new email if it was changed
                st.session_state["email"] = email_input
                st.session_state["page"] = "Dashboard"
                st.rerun()

            except Exception as e:
                st.error(f"❌ Error: {e}")
            finally:
                cur.close()
                conn.close()
