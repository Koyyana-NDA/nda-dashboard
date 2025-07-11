from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from auth import login_check
from file_upload import router as upload_router

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up CORS and templates
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

class JobData(BaseModel):
    job_code: str
    total_invoiced: float
    total_costs: float
    cost_to_come: float
    amended_contract_value: float
    unpaid_amount: float
    forecasted_margin: float

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

@app.get("/", response_class=HTMLResponse)
def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def handle_login(request: Request, username: str = Form(...), password: str = Form(...)):
    role = login_check(username, password)
    if role:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "username": username,
            "role": role
        })
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid credentials"
    })

@app.get("/jobs", response_model=List[JobData])
def get_jobs():
    return jobs

@app.get("/jobs/{job_code}", response_model=JobData)
def get_job(job_code: str):
    for job in jobs:
        if job.job_code == job_code:
            return job
    raise HTTPException(status_code=404, detail="Job not found")

app.include_router(upload_router)