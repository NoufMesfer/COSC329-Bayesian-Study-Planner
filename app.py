
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Bayesian Study Planner",
    page_icon="📚"
)

st.title("📚 Bayesian Study Planner")

st.write(
    "A personalized study planner using Bayesian networks."
)

st.subheader("Student Information")

# Ask for the exam date
exam_date = st.date_input(
    "When is your exam?",
    min_value=date.today()
)

# For now, use three database concepts
concepts = [
    "ER Diagrams",
    "SQL Queries",
    "Normalization"
]

st.subheader("Concept Difficulties")

# Store each difficulty using generic Bayesian network names
difficulties = {}

for i, concept in enumerate(concepts, start=1):
    difficulties[f"Concept{i}Difficulty"] = st.selectbox(
        f"How difficult is {concept}?",
        ["Easy", "Hard"]
    )

# Ask for stress level
stress = st.selectbox(
    "What is your current stress level?",
    ["Low", "High"]
)

# Calculate days remaining
days_remaining = (exam_date - date.today()).days

if st.button("Generate Study Plan"):

    # Prepare evidence for the Bayesian network
    evidence = {
        **difficulties,
        "Stress": stress,
        "DaysRemaining": (
            "Few" if days_remaining <= 3 else "Many"
        )
    }

    st.success("Your information has been recorded!")

    st.write("**Course:** Databases")

    for i, concept in enumerate(concepts, start=1):
        st.write(
            f"**{concept}:**",
            difficulties[f"Concept{i}Difficulty"]
        )

    st.write("**Stress Level:**", stress)
    st.write("**Exam Date:**", exam_date)
    st.write("**Days Remaining:**", days_remaining)

    st.subheader("Bayesian Network Evidence")
    st.write(evidence)

    st.info(
        "In the next stage, this evidence will be used "
        "to calculate exam readiness using Bayesian inference."
    )
