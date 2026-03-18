def life_insurance_calculator(age: int, income: int, debts: int, dependents: int) -> int:
    """Return recommended life insurance coverage.

    The calculation uses a simple rule of thumb: ten times income plus
    outstanding debts plus $100,000 for each dependent.
    Inputs must be non-negative or ``ValueError`` is raised.
    """
    values = [age, income, debts, dependents]
    if any(v < 0 for v in values):
        raise ValueError("All inputs must be non-negative")
    return income * 10 + debts + dependents * 100_000
