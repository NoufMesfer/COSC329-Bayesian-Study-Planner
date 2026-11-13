
# Utility scores for each possible study action
UTILITY_TABLE = {
    "Intense Study": {"High": 2, "Low": 9},
    "Light Review": {"High": 8, "Low": 5},
    "Rest": {"High": 10, "Low": -5},
}

# Adjust utilities based on the student's stress level
STRESS_ADJUSTMENTS = {
    "Low": {
        "Intense Study": 0,
        "Light Review": 0,
        "Rest": 0,
    },
    "High": {
        "Intense Study": -3,
        "Light Review": -1,
        "Rest": 2,
    },
}


def calculate_expected_utility(prob_high, stress, action):
    """Calculate the expected utility of one study action."""

    if not 0 <= prob_high <= 1:
        raise ValueError("Readiness probability must be between 0 and 1.")

    if stress not in STRESS_ADJUSTMENTS:
        raise ValueError("Stress must be Low or High.")

    if action not in UTILITY_TABLE:
        raise ValueError("Unknown study action.")

    prob_low = 1 - prob_high

    utility_high = UTILITY_TABLE[action]["High"]
    utility_low = UTILITY_TABLE[action]["Low"]

    expected_utility = (
        prob_high * utility_high
        + prob_low * utility_low
    )

    expected_utility += STRESS_ADJUSTMENTS[stress][action]

    return expected_utility


def calculate_all_utilities(prob_high, stress):
    """Calculate expected utilities for all available actions."""

    utilities = {}

    for action in UTILITY_TABLE:
        utilities[action] = calculate_expected_utility(
            prob_high, stress, action
        )

    return utilities


def recommend_action(prob_high, stress):
    """Select the action with Maximum Expected Utility."""

    utilities = calculate_all_utilities(prob_high, stress)

    best_action = max(utilities, key=utilities.get)

    return best_action, utilities
