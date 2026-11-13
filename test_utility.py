
import unittest

from utility import (
    calculate_expected_utility,
    calculate_all_utilities,
    recommend_action,
)


class TestExpectedUtility(unittest.TestCase):

    def test_intense_study_utility(self):
        # 53% high readiness, high stress
        result = calculate_expected_utility(
            0.53, "High", "Intense Study"
        )
        self.assertAlmostEqual(result, 2.29)

    def test_light_review_utility(self):
        result = calculate_expected_utility(
            0.53, "High", "Light Review"
        )
        self.assertAlmostEqual(result, 5.59)

    def test_rest_utility(self):
        result = calculate_expected_utility(
            0.53, "High", "Rest"
        )
        self.assertAlmostEqual(result, 4.95)

    def test_calculate_all_utilities(self):
        utilities = calculate_all_utilities(0.53, "High")

        self.assertEqual(len(utilities), 3)
        self.assertIn("Intense Study", utilities)
        self.assertIn("Light Review", utilities)
        self.assertIn("Rest", utilities)

    def test_recommend_light_review(self):
        action, utilities = recommend_action(0.53, "High")

        self.assertEqual(action, "Light Review")
        self.assertAlmostEqual(utilities[action], 5.59)

    def test_low_readiness_recommendation(self):
        # Very low readiness, low stress
        action, _ = recommend_action(0.0, "Low")

        self.assertEqual(action, "Intense Study")

    def test_high_readiness_recommendation(self):
        # Very high readiness, low stress
        action, _ = recommend_action(1.0, "Low")

        self.assertEqual(action, "Rest")

    def test_stress_changes_recommendation(self):
        low_stress_action, _ = recommend_action(0.7, "Low")
        high_stress_action, _ = recommend_action(0.7, "High")

        self.assertEqual(low_stress_action, "Light Review")
        self.assertEqual(high_stress_action, "Rest")

    def test_invalid_probability(self):
        with self.assertRaises(ValueError):
            recommend_action(-0.2, "Low")

        with self.assertRaises(ValueError):
            recommend_action(1.5, "High")

    def test_invalid_stress(self):
        with self.assertRaises(ValueError):
            recommend_action(0.5, "Medium")

    def test_invalid_action(self):
        with self.assertRaises(ValueError):
            calculate_expected_utility(
                0.5, "Low", "Unknown Action"
            )


if __name__ == "__main__":
    unittest.main()
