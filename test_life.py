import importlib.machinery
import pathlib
import sys
import types
import unittest


LIFE_PATH = pathlib.Path(__file__).with_name("life")
loader = importlib.machinery.SourceFileLoader("life_module", str(LIFE_PATH))
life = types.ModuleType(loader.name)
sys.modules[loader.name] = life
loader.exec_module(life)


class LifeCalculatorTests(unittest.TestCase):
    def test_income_multiplier_varies_by_age(self):
        self.assertEqual(life.income_multiplier(28), 15)
        self.assertEqual(life.income_multiplier(45), 10)
        self.assertEqual(life.income_multiplier(65), 5)

    def test_breakdown_offsets_savings(self):
        profile = life.Profile(age=35, income=100000, debts=200000, dependents=2, savings=50000, childcare_years=3)
        breakdown = life.coverage_breakdown(profile)
        self.assertEqual(breakdown["existing_assets_offset"], -50000)
        self.assertGreater(breakdown["income_replacement"], breakdown["education_fund"])

    def test_total_coverage_never_negative(self):
        profile = life.Profile(age=70, income=0, debts=0, dependents=0, savings=999999, childcare_years=0)
        self.assertEqual(life.life_insurance_calculator(profile), 0)

    def test_recommend_term_length_respects_bounds(self):
        self.assertEqual(life.recommend_term_length(30, 0), 15)
        self.assertEqual(life.recommend_term_length(25, 5), 30)

    def test_recommend_term_length_older_with_dependents(self):
        # age > 35, no age bonus; 2 dependents → baseline 25, clamped within [10, 30]
        self.assertEqual(life.recommend_term_length(40, 2), 25)

    def test_scenario_analysis_balanced_matches_calculator(self):
        profile = life.Profile(age=35, income=80000, debts=50000, dependents=1, savings=10000, childcare_years=2)
        scenarios = dict(life.scenario_analysis(profile))
        self.assertEqual(scenarios["Balanced plan"], life.life_insurance_calculator(profile))

    def test_scenario_analysis_ordering(self):
        profile = life.Profile(age=40, income=100000, debts=0, dependents=0)
        scenarios = life.scenario_analysis(profile)
        lean, balanced, future = [amt for _, amt in scenarios]
        self.assertLess(lean, balanced)
        self.assertLess(balanced, future)

    def test_childcare_bridge_zero_without_dependents(self):
        profile = life.Profile(age=40, income=60000, debts=0, dependents=0, childcare_years=5)
        breakdown = life.coverage_breakdown(profile)
        self.assertEqual(breakdown["childcare_bridge"], 0)


if __name__ == "__main__":
    unittest.main()
