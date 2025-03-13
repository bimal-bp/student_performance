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
