import pytest

from life_insurance import (
    DEPENDENT_SUPPORT_AMOUNT,
    FINAL_EXPENSE_BUFFER,
    life_insurance_calculator,
)


@pytest.mark.parametrize(
    ("age", "income", "debts", "dependents", "expected"),
    [
        (
            25,
            50_000,
            20_000,
            2,
            50_000 * 12 + 20_000 + 2 * DEPENDENT_SUPPORT_AMOUNT + FINAL_EXPENSE_BUFFER,
        ),
        (
            40,
            80_000,
            0,
            0,
            80_000 * 10 + FINAL_EXPENSE_BUFFER,
        ),
        (
            55,
            90_000,
            15_000,
            1,
            90_000 * 7 + 15_000 + DEPENDENT_SUPPORT_AMOUNT + FINAL_EXPENSE_BUFFER,
        ),
        (
            65,
            60_000,
            10_000,
            0,
            60_000 * 5 + 10_000 + FINAL_EXPENSE_BUFFER,
        ),
    ],
)
def test_calculator_recommends_coverage_by_age_band(age, income, debts, dependents, expected):
    assert life_insurance_calculator(age, income, debts, dependents) == expected


@pytest.mark.parametrize("field", ["age", "income", "debts", "dependents"])
def test_calculator_rejects_negative_values(field):
    values = {"age": 35, "income": 70_000, "debts": 5_000, "dependents": 1}
    values[field] = -1

    with pytest.raises(ValueError, match=field):
        life_insurance_calculator(**values)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("age", 30.5),
        ("income", "50000"),
        ("debts", None),
        ("dependents", True),
    ],
)
def test_calculator_rejects_non_integer_values(field, value):
    values = {"age": 35, "income": 70_000, "debts": 5_000, "dependents": 1}
    values[field] = value

    with pytest.raises(TypeError, match=field):
        life_insurance_calculator(**values)
