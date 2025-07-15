from fastapi import FastAPI, Request
from pydantic import BaseModel
from mission_planner import generate_mission
from threat_advisor import generate_advice
from debrief_analyzer import analyze_debrief
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputText(BaseModel):
    text: str

@app.post("/plan")
def plan_mission(data: InputText):
    result = generate_mission(data.text)
    return {"result": result}

@app.post("/advise")
def advise(data: InputText):
    result = generate_advice(data.text)
    return {"result": result}

@app.post("/debrief")
def debrief(data: InputText):
    result = analyze_debrief(data.text)
    return {"result": result}
