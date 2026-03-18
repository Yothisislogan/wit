import sys
import os

# Ensure project root is on path for local imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from life_insurance import life_insurance_calculator


def test_calculator_typical_case():
    result = life_insurance_calculator(30, 50000, 20000, 2)
    assert result == 50000 * 10 + 20000 + 2 * 100000


def test_calculator_zero_dependents_and_debts():
    result = life_insurance_calculator(40, 80000, 0, 0)
    assert result == 80000 * 10


def test_calculator_negative_input():
    with pytest.raises(ValueError):
        life_insurance_calculator(30, -50000, 1000, 1)
