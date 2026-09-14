import importlib
import sys

# Import the module without triggering interactive code
spec = importlib.util.spec_from_file_location('life', 'life.py')
life = importlib.util.module_from_spec(spec)
spec.loader.exec_module(life)


def test_basic_calculation():
    result = life.life_insurance_calculator(30, 50000, 10000, 0)
    assert result == 50000 * 10 + 10000


def test_with_dependents_and_debts():
    result = life.life_insurance_calculator(40, 60000, 20000, 2)
    assert result == 60000 * 10 + 20000
