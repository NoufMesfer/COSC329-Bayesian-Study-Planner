from utility import recommend_action
from bayesian_model import build_model, predict_readiness
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
    display_evidence = {
    concept: difficulties[f"Concept{i}Difficulty"]
    for i, concept in enumerate(concepts, start=1)
    }
    display_evidence["Stress"] = stress
    display_evidence["Days Remaining"] = evidence["DaysRemaining"]

    st.write(display_evidence)

    model = build_model()

    #perform bayes inference using student evidence
    result = predict_readiness(model, evidence)

    high_readiness = result.get_value(ExamReadiness="High")
    low_readiness = result.get_value(ExamReadiness="Low")
    st.subheader("Exam Readiness Prediction")
    st.write(f"High Readiness: {high_readiness:.2%}")
    st.write(f"Low Readiness: {low_readiness:.2%}")
    st.progress(float(high_readiness))
    # Calculate Maximum Expected Utility
    best_action, utilities = recommend_action(
    float(high_readiness),
    stress
    )

    st.subheader("Expected Utility Analysis")

    for action, utility in utilities.items():
        st.write(f"**{action}:** {utility:.2f}")

    st.subheader("Recommended Study Action")
    st.success(f"Recommended Action: {best_action}")

    st.write(
    f"This action has the highest expected utility "
    f"({utilities[best_action]:.2f}), based on your "
    f"exam readiness and stress level."
    )  


    st.info(
    "Exam readiness has been calculated using Bayesian inference. "
    )
