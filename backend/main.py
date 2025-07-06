from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.responses import RedirectResponse
from backend.quickbooks_auth import get_auth_client, get_qbo_client, ACCOUNTING_SCOPE
from backend.token_store import save_tokens

app = FastAPI()

# Let the browser talk to our backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Structure of job data
class JobData(BaseModel):
    job_code: str
    total_invoiced: float
    total_costs: float
    cost_to_come: float
    amended_contract_value: float
    unpaid_amount: float
    forecasted_margin: float

# Sample dummy job data
jobs = [
    JobData(
        job_code="AIS Daywork",
        total_invoiced=202600.75,
        total_costs=134184.86,
        cost_to_come=5769.14,
        amended_contract_value=202600.75,
        unpaid_amount=0,
        forecasted_margin=62646.75
    ),
    JobData(
        job_code="LAM Daywork",
        total_invoiced=32697.5,
        total_costs=22122.36,
        cost_to_come=0,
        amended_contract_value=32697.5,
        unpaid_amount=0,
        forecasted_margin=10575.14
    ),
    JobData(
        job_code="NDA0001",
        total_invoiced=15100,
        total_costs=8858.2,
        cost_to_come=0,
        amended_contract_value=15100,
        unpaid_amount=0,
        forecasted_margin=6241.8
    ),
    JobData(
        job_code="NDA0004",
        total_invoiced=3207734.78,
        total_costs=2662355.89,
        cost_to_come=42118.33,
        amended_contract_value=3246688.98,
        unpaid_amount=38954.2,
        forecasted_margin=542214.76
    )
]

@app.get("/login")
def login():
    auth_client = get_auth_client()
    auth_url = auth_client.get_authorization_url([ACCOUNTING_SCOPE])
    return RedirectResponse(auth_url)

@app.get("/callback")
def callback(request: Request):
    code = request.query_params.get("code")
    realm_id = request.query_params.get("realmId")

    if not code or not realm_id:
        return {"error": "Missing code or realm ID from QuickBooks"}

    auth_client = get_auth_client()
    try:
        auth_client.get_bearer_token(code, realm_id=realm_id)
        save_tokens(
            auth_client.access_token,
            auth_client.refresh_token,
            realm_id
        )
        return {"message": "Successfully connected to QuickBooks and tokens saved!", "realm_id": realm_id}
    except Exception as e:
        return {"error": str(e)}

@app.get("/jobs", response_model=List[JobData])
def get_jobs():
    return jobs

@app.get("/jobs/{job_code}", response_model=JobData)
def get_job(job_code: str):
    for job in jobs:
        if job.job_code == job_code:
            return job
    raise HTTPException(status_code=404, detail="Job not found")