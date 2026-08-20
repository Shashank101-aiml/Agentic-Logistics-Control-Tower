from fastapi import FastAPI
from pipeline.pipeline import run_pipeline

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Supply Chain Risk API running"}

@app.get("/risk/{city}")
def get_risk(city: str):
    return run_pipeline(city)
@app.get("/high-risk")
def high_risk():
    cities = ["London", "Singapore", "Dubai"]

    results = []
    for city in cities:
        data = run_pipeline(city)
        if data["risk_score"] > 50:
            results.append(data)

    return results