from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from engine import Engine
import os

app=FastAPI(title="AIRE Genesis 3 Immersion", version="2.0.0")
engine=Engine(seed=int(os.getenv("AIRE_SEED","814237")))
app.mount("/static", StaticFiles(directory="."), name="static")

class Action(BaseModel):
    action:str
    params:dict={}

@app.get("/")
def index(): return FileResponse("index.html")
@app.get("/api/health")
def health(): return {"status":"ok","version":app.version}
@app.post("/api/experiment/start")
def start(lives:int=50):
    if lives<1 or lives>10000: raise HTTPException(400,"lives must be 1..10000")
    return engine.start(lives)
@app.get("/api/observation")
def observation(): return engine.observation()
@app.post("/api/action")
def action(a:Action):
    try: return engine.step(a.action,a.params)
    except ValueError as e: raise HTTPException(400,str(e))
@app.get("/api/state")
def state(): return engine.public_state()
@app.get("/api/memory")
def memory(): return engine.memory_public()
@app.get("/api/experiments")
def experiments(): return engine.experiment_summary()
@app.get("/api/results")
def results(): return engine.results()
@app.get("/api/history")
def history(limit:int=200): return engine.history(limit)
