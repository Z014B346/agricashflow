# Main 

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from logic import generate_cashflow_forecast
from fastapi.responses import HTMLResponse

app = FastAPI(title="Agribusiness Cash Flow Forecaster API")

@app.get("/", response_class=HTMLResponse)
def homepage():
    return '''
      <html>
      <head>
        <title>Agribusiness Cash Flow Forecaster API</title>
      </head>
      <body>
        <h1>Welcome to the Agribusiness Cash Flow Forecaster API</h1>
        <p>Use the links below to explore:</p>
        <ul>
          <li><a href="/docs">Swagger UI (Interactive API docs)</a></li>
          <li><a href="/redoc">ReDoc (API docs alternative)</a></li>
          <li><a href="/api/forecast/">POST Forecast (send data to get forecast)</a></li>
        </ul>
      </body>
    </html>
    '''

class FarmProfile(BaseModel):
    farm_name: str
    region: str
    enterprise: str
    hectares: float
    expected_yield_t_per_ha: float
    expected_price_per_tonne: float 
    fixed_expenses: float
    variable_costs_per_hectare: float
    loan_balance: float 
    loan_rate: float
    loan_term_years: int
    start_month: str
    years_forecasted: int 

class ForecastResponse(BaseModel):
    monthly_cash_flow: Dict[str, float]
    monthly_cumulative: Dict[str, float]
    flagged_months: list[str]
    yearly_cumulative: Dict[str, Union[float, int]]
    yearly_net: Dict[str, Union[float,int]]

@app.post("/api/forecast/", response_model=ForecastResponse)
def forecast_cash_flow(request: FarmProfile):
    result = generate_cashflow_forecast(
        hectares=request.hectares,
        expected_yield_t_per_ha=request.expected_yield_t_per_ha,
        price_per_tonne=request.expected_price_per_tonne,  
        fixed_expenses=request.fixed_expenses,
        variable_costs_per_ha=request.variable_costs_per_hectare,
        loan_balance=request.loan_balance,
        loan_rate=request.loan_rate,  
        loan_term_years=request.loan_term_years,
        start_month=request.start_month,
        years_forecasted=request.years_forecasted
    )
    return result
    
class LoanRequest(BaseModel):
    loan_balance: float 
    loan_rate: float
    loan_term_years: float

class LoanResponse(BaseModel):
    monthly_repayment: float
    total_repayment: float

class ExpenseEstimateRequest(BaseModel):
    region: str
    enterprise: str
    hectares: float

class ExpenseEstimateResponse(BaseModel):
    fixed_costs: float
    variable_costs_per_hectare: float
    total_estimated_costs: float

class HealthScoreResponse(BaseModel):
    score: str
    notes: Optional[str]
    
    