"""Utilities for estimating life insurance coverage needs."""

from __future__ import annotations

from numbers import Integral

DEPENDENT_SUPPORT_AMOUNT = 100_000
FINAL_EXPENSE_BUFFER = 15_000


def _validate_non_negative_int(name: str, value: int) -> int:
    """Return ``value`` when it is a non-negative integer.

    ``bool`` values are rejected even though ``bool`` is a subclass of ``int``.
    """
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise TypeError(f"{name} must be an integer")
    if value < 0:
        raise ValueError(f"{name} must be non-negative")
    return int(value)


def _income_multiplier(age: int) -> int:
    """Return the earnings replacement multiplier for the given age."""
    if age < 30:
        return 12
    if age < 45:
        return 10
    if age < 60:
        return 7
    return 5


def life_insurance_calculator(age: int, income: int, debts: int, dependents: int) -> int:
    """Estimate recommended life insurance coverage.

    The estimate combines:
    - age-based income replacement,
    - outstanding debts,
    - support for each dependent, and
    - a small final-expense buffer.
    """
    age = _validate_non_negative_int("age", age)
    income = _validate_non_negative_int("income", income)
    debts = _validate_non_negative_int("debts", debts)
    dependents = _validate_non_negative_int("dependents", dependents)

    return (
        income * _income_multiplier(age)
        + debts
        + dependents * DEPENDENT_SUPPORT_AMOUNT
        + FINAL_EXPENSE_BUFFER
    )
