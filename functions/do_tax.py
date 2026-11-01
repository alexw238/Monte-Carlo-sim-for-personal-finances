def do_tax(income):
    """
    Function to calculate the tax on a given income. Using the UK tax bands
    for the 2026/27 tax year.
    imputs:
        income: float - the income to calculate tax on
    outputs:
        tax: float - the amount of tax to pay on the given income
    """

    income = round(income, 2)

    if income <= 12570:
        tax = 0
        return tax

    elif income <= 57270:
        tax = income * 0.2
        return tax

    elif income <= 125140:
        tax = (income - 57270) * 0.4
        tax += (57270 - 12570) * 0.2
        return tax

    elif income > 125140:
        tax = (income - 125140) * 0.45
        tax += (125140 - 57270) * 0.4
        tax += (57270 - 12570) * 0.2
        return tax

    else:
        raise TypeError("Income must be a float or int."
                         "Please check the input type.")