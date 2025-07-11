
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

from auth import login_check
from file_upload import router as upload_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def show_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    role = login_check(username, password)
    if role:
        return templates.TemplateResponse("dashboard.html", {"request": request, "username": username, "role": role})
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

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
    )
]

@app.get("/jobs", response_model=List[JobData])
def get_jobs():
    return jobs

app.include_router(upload_router)