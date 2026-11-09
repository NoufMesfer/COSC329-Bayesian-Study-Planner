
from itertools import product

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


#Bayeian net structure
def build_model():

    model = DiscreteBayesianNetwork([
    ("Concept1Difficulty", "Mastery"),
    ("Concept2Difficulty", "Mastery"),
    ("Concept3Difficulty", "Mastery"),
    ("Mastery", "ExamReadiness"),
    ("Stress", "ExamReadiness"),
    ("DaysRemaining", "ExamReadiness")
    ])

    
    #prior probabilities
    difficulties = [
        "Concept1Difficulty",
        "Concept2Difficulty",
        "Concept3Difficulty",
    ]

    difficulty_cpds = []

    for concept in difficulties:
        cpd = TabularCPD(
            variable=concept,
            variable_card=2,
            values=[[0.5], [0.5]],
            state_names={
                concept: ["Easy", "Hard"]
            },
        )
        difficulty_cpds.append(cpd)

    stress_cpd = TabularCPD(
        variable="Stress",
        variable_card=2,
        values=[[0.6], [0.4]],
        state_names={
            "Stress": ["Low", "High"]
        },
    )

    days_cpd = TabularCPD(
        variable="DaysRemaining",
        variable_card=2,
        values=[[0.5], [0.5]],
        state_names={
            "DaysRemaining": ["Few", "Many"]
        },
    )

    #Mastery CPT

    #P(Mastery=High), indexed by the number of hard concepts
    mastery_probabilities = {
        0: 0.85,
        1: 0.65,
        2: 0.45,
        3: 0.15,
    }
    mastery_high = []

    for combination in product(
        ["Easy", "Hard"], repeat=3
    ):
        number_hard = combination.count("Hard")
        mastery_high.append(
            mastery_probabilities[number_hard]
        )

    mastery_low = [
        1 - p for p in mastery_high
    ]

    mastery_cpd = TabularCPD(
        variable="Mastery",
        variable_card=2,
        values=[mastery_low, mastery_high],
        evidence=difficulties,
        evidence_card=[2, 2, 2],
        state_names={
            "Mastery": ["Low", "High"],
            **{
                concept: ["Easy", "Hard"]
                for concept in difficulties
            },
        },
    )

    #ExamReadiness CPT
    #Each column corresponds to: Mastery, Stress, DaysRemaining

    readiness_high = [
        0.40, 0.55, 0.20, 0.35,
        0.80, 0.95, 0.60, 0.75,
    ]

    readiness_low = [
        1 - p for p in readiness_high
    ]

    readiness_cpd = TabularCPD(
        variable="ExamReadiness",
        variable_card=2,
        values=[readiness_low, readiness_high],
        evidence=[
            "Mastery",
            "Stress",
            "DaysRemaining",
        ],
        evidence_card=[2, 2, 2],
        state_names={
            "ExamReadiness": ["Low", "High"],
            "Mastery": ["Low", "High"],
            "Stress": ["Low", "High"],
            "DaysRemaining": ["Few", "Many"],
        },
    )


    model.add_cpds(
        *difficulty_cpds,
        mastery_cpd,
        stress_cpd,
        days_cpd,
        readiness_cpd,
    )

    assert model.check_model()
    return model

def predict_readiness(model, evidence):

    inference = VariableElimination(model)

    result = inference.query(
        variables=["ExamReadiness"],
        evidence=evidence,
        show_progress=False,
    )

    return result


#Testing
if __name__ == "__main__":

    model = build_model()

    print("Bayesian network is valid!")

    evidence = {
    "Concept1Difficulty": "Hard",  # ER Diagrams
    "Concept2Difficulty": "Hard",  # SQL Queries
    "Concept3Difficulty": "Hard",  # Normalization
    "Stress": "High",
    "DaysRemaining": "Few",
    }

    result = predict_readiness(model, evidence)

    print("\nStudent scenario:")
    print(evidence)

    print("\nExam readiness probabilities:")
    print(result)
