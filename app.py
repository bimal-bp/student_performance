import streamlit as st
import psycopg2
from psycopg2 import sql
import numpy as np
import pickle
import random

# Database Connection String
DB_URL = "postgresql://neondb_owner:npg_Qv3eN1JblqYo@ep-tight-sun-a8z1f6um-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DB_URL)

# Subject importance ratings
subject_ratings = {
    # Computer Science
    "Programming": 10, "Data Structures & Algorithms": 10, "Operating Systems": 9,
    "Computer Networks": 9, "Database Management Systems": 9, "Software Engineering": 8,
    "Web Technologies": 8, "Compiler Design": 7, "Object-Oriented Programming": 9,
    "Cryptography & Network Security": 8, "Software Testing": 7, "Data Mining & Data Warehousing": 8,
    "Business Communication & Ethics": 6, "Business Analytics": 7, "Digital Marketing": 7,

    # Artificial Intelligence
    "Artificial Intelligence": 10, "Machine Learning": 10, "Deep Learning": 9,
    "Data Science & Analytics": 9, "Natural Language Processing": 8, "Neural Networks": 9,
    "Reinforcement Learning": 8, "Computer Vision": 8, "Linear Algebra for ML": 9,
    "Data Visualization": 9,

    # Electrical Engineering
    "Circuit Theory": 8, "Digital Logic Design": 9, "Analog & Digital Electronics": 9,
    "Signals & Systems": 8, "Microprocessors & Microcontrollers": 9, "Communication Systems": 8,
    "VLSI Design": 7, "Antennas & Wave Propagation": 7, "Embedded Systems": 9,
    "Optical Communication": 7, "IoT & Wireless Sensor Networks": 8, "Electrical Circuits": 8,
    "Control Systems": 9, "Power Systems": 8, "Electrical Machines": 8, "Power Electronics": 9,
    "Digital Signal Processing": 9, "High Voltage Engineering": 7, "Renewable Energy Systems": 8,
    "Industrial Automation": 8,

    # Mechanical Engineering
    "Engineering Mechanics": 9, "Strength of Materials": 9, "Thermodynamics": 9,
    "Fluid Mechanics": 8, "Manufacturing Processes": 8, "Heat & Mass Transfer": 9,
    "Machine Design": 9, "Robotics": 8, "CAD/CAM": 9, "Automotive Engineering": 7,
    "Industrial Engineering": 8,

    # Civil Engineering
    "Structural Analysis": 9, "Surveying": 8, "Geotechnical Engineering": 9,
    "Construction Materials": 8, "Transportation Engineering": 8, "Environmental Engineering": 8,
    "Hydrology & Water Resources": 7, "Building Design & Architecture": 8, "Earthquake Engineering": 8,

    # Common subjects
    "Engineering Mathematics": 10, "Engineering Physics": 8, "Engineering Chemistry": 6,
    "Basic Electrical and Electronical Engineering": 7, "Big Data Technologies": 8,
    "Cloud Computing": 8, "Cyber Security": 8, "Blockchain Technology": 7, "IoT (Internet of Things)": 7,
    "Introduction to AI & ML": 8, "Probability & Statistics": 10, "Engineering Drawing": 7,
}

def allocate_study_time(selected_subjects, total_hours, efficiency_level, problem_solving):
    # Define efficiency and problem-solving factors
    efficiency_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[efficiency_level]
    problem_solving_factor = {"low": 0.8, "intermediate": 1.0, "high": 1.2}[problem_solving]
    
    # Get ratings for selected subjects (default to 5 if not found)
    ratings = np.array([subject_ratings.get(sub, 5) for sub in selected_subjects])
    
    # Calculate weighted ratings
    weighted_ratings = ratings * efficiency_factor * problem_solving_factor
    
    # Normalize weights
    normalized_weights = weighted_ratings / np.sum(weighted_ratings)
    
    # Allocate time in hours
    allocated_times_hours = normalized_weights * total_hours
    
    # Convert decimal hours to hours and minutes
    allocated_times = {}
    for subject, time_hours in zip(selected_subjects, allocated_times_hours):
        hours = int(time_hours)
        minutes = int((time_hours - hours) * 60)
        allocated_times[subject] = f"{hours}h {minutes}m"
    
    return allocated_times
    
def student_info():
    st.title("Learn Mate - Student Performance Application")
    st.header("Student Information")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100)
    email = st.text_input("Email")
    mobile_number = st.text_input("Mobile Number")

    st.subheader("Select Your Branch")
    branch = st.selectbox(
        "Choose your branch",
        options=["Computer Science", "Artificial Intelligence", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering"],
        key="branch"
    )

    common_subjects = [
        "Engineering Mathematics", "Engineering Physics", "Engineering Chemistry",
        "Basic Electrical and Electronical Engineering", "Web Technologies", "Programming",
        "Data Structures & Algorithms", "Operating Systems", "Computer Networks",
        "Cryptography & Network Security", "Big Data Technologies", "Cloud Computing",
        "Cyber Security", "Blockchain Technology", "IoT (Internet of Things)",
        "Introduction to AI & ML", "Data Science & Analytics", "Probability & Statistics",
        "Engineering Drawing"
    ]

branch_subjects = {
    "Computer Science": [
        "Advanced Programming", "Database Management Systems", "Software Engineering",
        "Machine Learning", "Artificial Intelligence", "Computer Architecture",
        "Programming", "Data Structures & Algorithms", "Operating Systems",
        "Computer Networks", "Web Technologies", "Compiler Design",
        "Object-Oriented Programming", "Cryptography & Network Security",
        "Software Testing", "Data Mining & Data Warehousing",
        "Business Communication & Ethics", "Business Analytics", "Digital Marketing"
    ],
    "Artificial Intelligence": [
        "Deep Learning", "Natural Language Processing", "Computer Vision",
        "Reinforcement Learning", "AI Ethics", "Robotics", "Artificial Intelligence",
        "Machine Learning", "Data Science & Analytics", "Neural Networks",
        "Linear Algebra for ML", "Data Visualization"
    ],
    "Electrical Engineering": [
        "Circuit Theory", "Power Systems", "Control Systems", "Signal Processing",
        "Microelectronics", "Renewable Energy Systems", "Digital Logic Design",
        "Analog & Digital Electronics", "Signals & Systems", "Microprocessors & Microcontrollers",
        "Communication Systems", "VLSI Design", "Antennas & Wave Propagation",
        "Embedded Systems", "Optical Communication", "IoT & Wireless Sensor Networks",
        "Electrical Circuits", "Electrical Machines", "Power Electronics",
        "Digital Signal Processing", "High Voltage Engineering", "Industrial Automation"
    ],
    "Mechanical Engineering": [
        "Thermodynamics", "Fluid Mechanics", "Solid Mechanics", "Manufacturing Processes",
        "Heat Transfer", "Machine Design", "Engineering Mechanics", "Strength of Materials",
        "Heat & Mass Transfer", "Robotics", "CAD/CAM", "Automotive Engineering",
        "Industrial Engineering"
    ],
    "Civil Engineering": [
        "Structural Analysis", "Geotechnical Engineering", "Transportation Engineering",
        "Environmental Engineering", "Construction Management", "Hydrology",
        "Surveying", "Construction Materials", "Hydrology & Water Resources",
        "Building Design & Architecture", "Earthquake Engineering"
    ]
}

    all_subjects = common_subjects + branch_subjects.get(branch, [])
    selected_subjects = st.multiselect("Choose your subjects (select up to 10)", options=all_subjects, default=all_subjects[:10], key="subjects")

    st.subheader("Efficiency Levels")
    col1, col2 = st.columns(2)
    with col1:
        coding_eff = st.selectbox("Coding Efficiency", ["low", "intermediate", "high"])
        math_eff = st.selectbox("Math Efficiency", ["low", "intermediate", "high"])
    with col2:
        problem_solving_eff = st.selectbox("Problem Solving Efficiency", ["low", "intermediate", "high"])
        conceptual_understanding = st.selectbox("Conceptual Understanding", ["low", "intermediate", "high"])
        time_management = st.selectbox("Time Management", ["low", "intermediate", "high"])

    study_time = st.number_input("Total Study Time Per Week (hours)", min_value=1, max_value=168)

    if st.button("Save Information"):
        if not email:
            st.error("Please enter an email.")
        else:
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                subjects_str = ", ".join(selected_subjects)
                cur.execute(
                    sql.SQL("""
                        INSERT INTO students (name, age, email, mobile_number, coding_efficiency, math_efficiency, 
                        problem_solving_efficiency, conceptual_understanding, time_management, selected_subjects, study_time_per_week, branch)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO UPDATE SET 
                        name = EXCLUDED.name, age = EXCLUDED.age, mobile_number = EXCLUDED.mobile_number,
                        coding_efficiency = EXCLUDED.coding_efficiency, math_efficiency = EXCLUDED.math_efficiency,
                        problem_solving_efficiency = EXCLUDED.problem_solving_efficiency,
                        conceptual_understanding = EXCLUDED.conceptual_understanding,
                        time_management = EXCLUDED.time_management, selected_subjects = EXCLUDED.selected_subjects,
                        study_time_per_week = EXCLUDED.study_time_per_week, branch = EXCLUDED.branch
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

    def dashboard():
        st.header("Student Dashboard")
    
        if "email" not in st.session_state:
            st.warning("Please log in to view your dashboard.")
            return
    
        email = st.session_state["email"]
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "SELECT name, age, email, mobile_number, coding_efficiency, math_efficiency, problem_solving_efficiency, selected_subjects, study_time_per_week, branch FROM students WHERE email = %s",
                (email,),
            )
            student = cur.fetchone()
            cur.close()
            conn.close()
    
            if student:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("### Student Information")
                    st.write(f"**Name:** {student[0]}")
                    st.write(f"**Age:** {student[1]}")
                    st.write(f"**Email:** {student[2]}")
                    st.write(f"**Mobile Number:** {student[3]}")
                    st.write(f"**Study Time Per Week:** {student[8]} h/w")
                    st.write(f"**Branch:** {student[9]}")
    
                with col2:
                    st.write("### Study Time Allocation")
                    selected_subjects = student[7].split(", ")
                    study_time = student[8]
                    coding_eff = student[4]
                    problem_solving_eff = student[6]
                    study_allocation = allocate_study_time(selected_subjects, study_time, coding_eff, problem_solving_eff)
                    for subject, hours in study_allocation.items():
                        st.write(f"- **{subject}:** {hours} h/w")
    
                st.markdown("---")
                col3, col4, col5, col6 = st.columns(4)  # Added a new column for the "Update Profile" button
                with col3:
                    if st.button("Predict Future Score 🎯"):
                        st.session_state["page"] = "Predict Future Score"
                        st.rerun()
                with col4:
                    if st.button("Take a Quiz 📝"):
                        st.session_state["page"] = "Quiz"
                        st.rerun()
                with col5:
                    if st.button("Study Content 📚"):
                        st.session_state["page"] = "Study Content"
                        st.rerun()
                with col6:
                    if st.button("Update Profile ✏️"):  # New button to update profile
                        st.session_state["page"] = "Student Info"
                        st.rerun()
            else:
                st.warning("No records found for the logged-in user.")
        except Exception as e:
            st.error(f"❌ Error loading dashboard: {e}")

def predict_future_score():
    st.header("Predict Future Score 🎯")
    st.write("Please provide additional details to predict your future score.")

    age = st.number_input("Age", min_value=1, max_value=100, value=st.session_state.get("age", 20))
    study_time_weekly = st.number_input("Study Time Per Week (hours)", min_value=1, max_value=168, value=st.session_state.get("study_time_per_week", 20))
    absences = st.number_input("Number of Absences", min_value=0, max_value=100, value=0)
    tutoring = st.selectbox("Do you receive tutoring?", ["No", "Yes"])
    extracurricular = st.selectbox("Do you participate in extracurricular activities?", ["No", "Yes"])
    sports = st.selectbox("Do you participate in sports?", ["No", "Yes"])
    music = st.selectbox("Do you participate in music activities?", ["No", "Yes"])
    volunteering = st.selectbox("Do you volunteer?", ["No", "Yes"])

    if st.button("Predict Grade"):
        # Prepare input data for the model
        tutoring = 1 if tutoring == "Yes" else 0
        extracurricular = 1 if extracurricular == "Yes" else 0
        sports = 1 if sports == "Yes" else 0
        music = 1 if music == "Yes" else 0
        volunteering = 1 if volunteering == "Yes" else 0

        user_data = [age, study_time_weekly, absences, tutoring, extracurricular, sports, music, volunteering]

        # Load the trained model
        with open('model (6).pkl', 'rb') as file:
            model = pickle.load(file)

        # Make a prediction
        predicted_grade = model.predict([user_data])

        # Display the result
        st.write(f"**Predicted Grade:** {predicted_grade[0]}")

        # Provide suggestions based on the predicted grade
        if predicted_grade[0] == 1:
            st.success("You are doing great! Keep up the good work.")
        elif predicted_grade[0] == 2:
            st.warning("You are doing well, but there is room for improvement. Consider increasing your study time or seeking tutoring.")
        else:
            st.error("You may need to make significant changes to improve your performance. Consider seeking tutoring, reducing absences, and increasing study time.")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def quiz_section():
    st.header("Quiz Section")
    
    try:
        with open('quiz_data.pkl', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        st.error("The questions file was not found. Please ensure 'quiz_data.pkl' is in the correct directory.")
        return

    # Allow the user to select a branch
    branch = st.selectbox("Choose a branch for the quiz:", list(data.keys()))
    
    if 'quiz_started' not in st.session_state:
        st.session_state.update({
            'quiz_started': False,
            'current_question': 0,
            'user_answers': [],
            'score': 0,
            'selected_answer': None,
            'selected_branch': None
        })

    if not st.session_state['quiz_started']:
        if st.button("Start Quiz"):
            st.session_state['quiz_started'] = True
            st.session_state['selected_branch'] = branch
            st.session_state['selected_questions'] = random.sample(data[branch], min(30, len(data[branch])))  # Select up to 30 questions

    if st.session_state['quiz_started']:
        selected_questions = st.session_state['selected_questions']
        if st.session_state['current_question'] < len(selected_questions):
            question = selected_questions[st.session_state['current_question']]
            st.write(f"**Question {st.session_state['current_question'] + 1}:** {question['question']}")
            user_answer = st.radio("Select your answer:", question['options'], key=f"q{st.session_state['current_question']}", index=None)
            
            if st.button("Submit Answer"):
                if user_answer is not None:
                    st.session_state['selected_answer'] = user_answer
                    if user_answer[0] == question['answer']:  # Compare the first character (e.g., "A", "B")
                        st.session_state['score'] += 1
                    st.session_state['user_answers'].append(user_answer)
                    st.session_state['current_question'] += 1
                    st.session_state['selected_answer'] = None
                    st.rerun()
                else:
                    st.warning("Please select an answer before submitting.")
        else:
            st.write("### Quiz Ended!")
            st.write(f"**Your Score:** {st.session_state['score']}/{len(selected_questions)}")
            st.write("### Review Your Answers:")
            for i, (question, user_answer) in enumerate(zip(selected_questions, st.session_state['user_answers'])):
                st.write(f"**Question {i + 1}:** {question['question']}")
                st.write(f"**Your Answer:** {user_answer}")
                st.write(f"**Correct Answer:** {question['answer']}")
                st.write("---")
            if st.button("Restart Quiz"):
                st.session_state.update({
                    'quiz_started': False,
                    'current_question': 0,
                    'user_answers': [],
                    'score': 0,
                    'selected_answer': None,
                    'selected_branch': None
                })
                st.rerun()

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def add_study_content():
    st.header("Study Materials")

    # Define the study content links for each subject
    study_content_links = {
        # Common Subjects
        "Engineering Mathematics": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=ME564_Lecture_1",
            "Online Course": "https://www.coursera.org/specializations/mathematics-for-engineers",
            "Study Material": "https://nptel.ac.in/courses/111/105/111105080/"
        },
        "Engineering Physics": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Engineering_Physics_Introduction",
            "Online Course": "https://ocw.mit.edu/courses/physics/8-01sc-physics-i-classical-mechanics-fall-2010/",
            "Study Material": "https://nptel.ac.in/courses/115/106/115106005/"
        },
        "Engineering Chemistry": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Engineering_Chemistry_Introduction",
            "Online Course": "https://ocw.mit.edu/courses/chemistry/5-111sc-principles-of-chemical-science-fall-2014/",
            "Study Material": "https://nptel.ac.in/courses/103/106/103106006/"
        },
        "Programming": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Programming_Basics_Introduction",
            "Online Course": "https://www.edx.org/course/introduction-to-computer-science",
            "Study Material": "https://www.coursera.org/learn/python"
        },
        "Probability & Statistics": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Probability_Statistics_Introduction",
            "Online Course": "https://www.khanacademy.org/math/statistics-probability",
            "Study Material": "https://ocw.mit.edu/courses/mathematics/18-05-introduction-to-probability-and-statistics-spring-2014/"
        },
        "Basic Electrical Engineering": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=ELECTRICITY_FOR_BEGINNERS",
            "Online Course": "https://www.khanacademy.org/science/electrical-engineering",
            "Study Material": "https://www.electronics-tutorials.ws/"
        },
        "Engineering Drawing": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Introduction_to_Engineering_Drawing_1",
            "Online Course": "https://ocw.mit.edu/courses/mechanical-engineering/2-007-design-and-manufacturing-i-spring-2009/",
            "Study Material": "https://www.engineeringdrawing.org/"
        },
        "Engineering Economics & Financial Management": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Engineering_Economics_Introduction",
            "Online Course": "https://www.edx.org/course/engineering-economic-analysis",
            "Study Material": "https://courses.lumenlearning.com/suny-ece/"
        },

        # CSE Subjects
        "Data Structures & Algorithms": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Data_Structures_Introduction",
            "Online Course": "https://www.coursera.org/specializations/data-structures-algorithms",
            "Study Material": "https://www.geeksforgeeks.org/data-structures/"
        },
        "Operating Systems": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Operating_System_Complete_Course",
            "Online Course": "https://www.edx.org/course/operating-systems-and-system-programming",
            "Study Material": "https://www.tutorialspoint.com/operating_system/index.htm"
        },
        "Computer Networks": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Computer_Networking_Full_Course",
            "Online Course": "https://www.edx.org/course/computer-networks",
            "Study Material": "https://www.geeksforgeeks.org/computer-network-tutorials/"
        },
        "Database Management Systems": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Database_Management_Systems_Full_Course",
            "Online Course": "https://www.edx.org/course/databases-relational-databases-and-sql",
            "Study Material": "https://www.javatpoint.com/dbms-tutorial"
        },
        "Software Engineering": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Software_Engineering_Full_Course",
            "Online Course": "https://www.coursera.org/learn/software-processes-and-agile-practices",
            "Study Material": "https://www.tutorialspoint.com/software_engineering/index.htm"
        },
        "Web Technologies": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Full_Stack_Web_Development_Tutorial",
            "Online Course": "https://www.udemy.com/course/the-web-developer-bootcamp/",
            "Study Material": "https://developer.mozilla.org/en-US/docs/Web/Tutorials"
        },
        "Compiler Design": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Compiler_Design_Full_Course",
            "Online Course": "https://www.edx.org/course/compilers",
            "Study Material": "https://www.geeksforgeeks.org/compiler-design-tutorials/"
        },
        "Cloud Computing": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Cloud_Computing_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/cloud-computing",
            "Study Material": "https://www.tutorialspoint.com/cloud_computing/index.htm"
        },
        "Cyber Security": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Cyber_Security_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/cyber-security",
            "Study Material": "https://www.geeksforgeeks.org/cyber-security-tutorials/"
        },
        "Blockchain Technology": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Blockchain_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/blockchain",
            "Study Material": "https://www.tutorialspoint.com/blockchain/index.htm"
        },
        "Internet of Things (IoT)": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=IoT_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/internet-of-things",
            "Study Material": "https://www.tutorialspoint.com/internet_of_things/index.htm"
        },
        "Artificial Intelligence": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Artificial_Intelligence_Full_Course",
            "Online Course": "https://www.coursera.org/learn/ai-for-everyone",
            "Study Material": "https://www.tutorialspoint.com/artificial_intelligence/index.htm"
        },
        "Machine Learning": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Machine_Learning_Full_Course",
            "Online Course": "https://www.coursera.org/learn/machine-learning",
            "Study Material": "https://www.geeksforgeeks.org/machine-learning-tutorials/"
        },
        "Data Science": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Data_Science_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/applied-data-science-python",
            "Study Material": "https://www.geeksforgeeks.org/data-science-tutorials/"
        },
        "Big Data Technologies": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Big_Data_Technologies_Introduction",
            "Online Course": "https://www.coursera.org/specializations/big-data",
            "Study Material": "https://developer.ibm.com/technologies/big-data/"
        },
        "Natural Language Processing (NLP)": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Natural_Language_Processing_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/natural-language-processing",
            "Study Material": "https://nlp.stanford.edu/online/courses/"
        },
        "Computer Vision": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Computer_Vision_Full_Course",
            "Online Course": "https://www.udacity.com/course/introduction-to-computer-vision--ud810",
            "Study Material": "https://www.geeksforgeeks.org/computer-vision-tutorials/"
        },
        "Reinforcement Learning": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Reinforcement_Learning_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/reinforcement-learning",
            "Study Material": "https://www.deepmind.com/learning-resources"
        },
        "Neural Networks": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Neural_Networks_Full_Course",
            "Online Course": "https://www.coursera.org/learn/neural-networks-deep-learning",
            "Study Material": "https://www.tutorialspoint.com/neural_networks/index.htm"
        },
        "Linear Algebra for Machine Learning": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Linear_Algebra_Math_for_Machine_Learning",
            "Online Course": "https://www.coursera.org/learn/linear-algebra-machine-learning",
            "Study Material": "https://machinelearningmastery.com/linear-algebra-for-machine-learning/"
        },
        "Object-Oriented Programming (OOP)": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=OOP_Concepts_in_C#",
            "Online Course": "https://www.softwaretestinghelp.com/object-oriented-programming-in-java/",
            "Study Material": "https://www.softwaretestinghelp.com/oop-concepts-in-c#/"
        },
        "Cryptography & Network Security": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Cryptography_and_Network_Security_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/cryptography",
            "Study Material": "https://www.tutorialspoint.com/security_testing/index.htm"
        },
        "Software Testing": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Security_Testing_Tutorial",
            "Online Course": "https://www.coursera.org/specializations/software-testing",
            "Study Material": "https://www.softwaretestingmaterial.com/"
        },
        "Data Mining & Data Warehousing": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Data_Mining_and_Data_Warehousing_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/data-warehousing",
            "Study Material": "https://www.geeksforgeeks.org/data-mining-and-warehousing/"
        },
        "Business Communication & Ethics": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Simplilearn_Business_Communication_Skills",
            "Online Course": "https://www.udemy.com/course/free-communication-skills-course/",
            "Study Material": "https://www.coursera.org/learn/communication-skills"
        },
        "Business Analytics": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=Business_Analytics_Full_Course",
            "Online Course": "https://www.coursera.org/specializations/business-analytics",
            "Study Material": "https://www.tutorialspoint.com/business_analytics/index.htm"
        },
        "Digital Marketing": {
            "YouTube Tutorial": "https://www.youtube.com/watch?v=The_Effect_of_Cryptocurrency_on_Digital_Marketing",
            "Online Course": "https://www.udemy.com/course/top-digital-marketing-courses/",
            "Study Material": "https://www.mdpi.com/journal/sustainability/special_issues/digital_marketing"
        },
    }

    # Dropdown to select a subject
    selected_subject = st.selectbox("Select a subject", options=list(study_content_links.keys()))

    # Display the links for the selected subject
    if selected_subject:
        st.write(f"### {selected_subject}")
        for resource_type, link in study_content_links[selected_subject].items():
            st.write(f"- **{resource_type}:** [{link}]({link})")

    if st.button("Back to Dashboard"):
        st.session_state["page"] = "Dashboard"
        st.rerun()

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Student Info"

    if st.session_state["page"] == "Student Info":
        student_info()
    elif st.session_state["page"] == "Dashboard":
        dashboard()
    elif st.session_state["page"] == "Quiz":
        quiz_section()
    elif st.session_state["page"] == "Study Content":
        add_study_content()
    elif st.session_state["page"] == "Predict Future Score":
        predict_future_score()

if __name__ == "__main__":
    main()
