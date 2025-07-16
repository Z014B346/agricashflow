# Logic

from typing import Dict, List
import calendar

# Assumptions:
# Payment only comes once a year, in the fourth month after start_month. See comment in function where this applies.

def calculate_monthly_repayment(loan_balance: float, loan_rate: float, loan_term_years: int) -> float:
    r = (loan_rate / 100) / 12
    n = loan_term_years * 12
    if r == 0:
        return loan_balance / n
    return loan_balance * r * (1 + r) ** n / ((1 + r) ** n - 1)

def generate_cashflow_forecast(
    hectares: float,
    expected_yield_t_per_ha: float,
    price_per_tonne: float,
    fixed_expenses: float,
    variable_costs_per_ha: float,
    loan_balance: float,
    loan_rate: float,
    loan_term_years: int,
    start_month: str,
    years_forecasted: int
) -> Dict[str, Dict]:

    gross_income = hectares * expected_yield_t_per_ha * price_per_tonne
    total_expenses = fixed_expenses + (variable_costs_per_ha * hectares)
    monthly_expenses = total_expenses / 12

    monthly_loan_payment = calculate_monthly_repayment(loan_balance, loan_rate, loan_term_years)

    months = list(calendar.month_name)[1:]
    start_index = months.index(start_month)
    reordered_months = months[start_index:] + months[:start_index]

    cash_flow = {}
    cumulative = {}
    running_total = 0

    # First year: month-by-month
    for i, month in enumerate(reordered_months):
        income = gross_income if i == 3 else 0  # Harvest income arrives in the 4th month
        expenses = monthly_expenses
        loan = monthly_loan_payment

        net = income - expenses - loan
        running_total += net
        cash_flow[month] = round(net, 2)
        cumulative[month] = round(running_total, 2)

    flagged_months = [m for m, v in cash_flow.items() if v < 0]

    # Multi-year cumulative projections (Year 2 to N) # Also included a net yearly income, not useful now but when used for risk projections will become more relevant
    yearly_cumulative = {}
    yearly_net = {}
    for year in range(2, years_forecasted + 1):
        annual_income = gross_income
        annual_expenses = total_expenses
        annual_loan = monthly_loan_payment * 12 if year <= loan_term_years else 0

        annual_net = annual_income - annual_expenses - annual_loan
        running_total += annual_net
        yearly_cumulative[f"Year {year}"] = round(running_total, 2)
        yearly_net[f"Year {year}"] = round(annual_net, 2)
  
    return {
        "monthly_cash_flow": cash_flow,
        "monthly_cumulative": cumulative,
        "flagged_months": flagged_months,
        "yearly_cumulative": yearly_cumulative,
        "yearly_net": yearly_net
    }
