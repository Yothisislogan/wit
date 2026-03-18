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


if __name__ == "__main__":
    unittest.main()
