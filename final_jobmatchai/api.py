from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from agent import run_agent
from db_tool import get_all, get_top3, get_by_name, delete_candidate
import io, sys

app = FastAPI()

# ✅ CORS MUST be here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    message: str

class NameRequest(BaseModel):
    name: str

# capture print output from agent
def capture_agent_output(command: str):
    buffer = io.StringIO()
    sys.stdout = buffer
    run_agent(command)
    sys.stdout = sys.__stdout__
    return buffer.getvalue()

@app.get("/")
def home():
    return {"message": "JobMatch AI API running"}

@app.post("/evaluate")
def evaluate(data: Query):
    output = capture_agent_output(data.message)
    return {"reasoning": output}

@app.get("/candidates")
def candidates():
    return get_all()

@app.get("/top3")
def top3():
    return get_top3()

@app.post("/search")
def search(data: NameRequest):
    return get_by_name(data.name)

@app.delete("/delete")
def delete(data: NameRequest):
    return {"message": delete_candidate(data.name)}