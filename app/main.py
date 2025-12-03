from __future__ import annotations

from datetime import datetime
from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, conint

app = FastAPI(title="Azure Forecast Demo", version="0.1.0")


templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class ForecastRequest(BaseModel):
    history: List[float]
    steps: conint(gt=0, le=50) = 7


class ForecastResponse(BaseModel):
    forecast: List[float]
    last_observation: float
    started_at: datetime
    completed_at: datetime


def extrapolate(history: List[float], steps: int) -> List[float]:
    if not history:
        raise ValueError("history must contain at least one value")

    if len(history) == 1:
        return [history[0]] * steps

    last = history[-1]
    diffs = [b - a for a, b in zip(history, history[1:])]
    avg_growth = sum(diffs) / len(diffs)

    forecast = []
    current = last
    for _ in range(steps):
        current += avg_growth
        forecast.append(round(current, 2))
    return forecast


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/forecast", response_model=ForecastResponse)
async def forecast(payload: ForecastRequest) -> ForecastResponse:
    started_at = datetime.utcnow()
    values = extrapolate(payload.history, payload.steps)
    completed_at = datetime.utcnow()
    return ForecastResponse(
        forecast=values,
        last_observation=payload.history[-1],
        started_at=started_at,
        completed_at=completed_at,
    )


def sample_dataset() -> List[float]:
    return [int(100 + i * 2 + (-1) ** i * 5) for i in range(14)]


@app.get("/api/sample", response_model=ForecastResponse)
async def sample_forecast() -> ForecastResponse:
    history = sample_dataset()
    steps = 7
    started_at = datetime.utcnow()
    values = extrapolate(history, steps)
    completed_at = datetime.utcnow()
    return ForecastResponse(
        forecast=values,
        last_observation=history[-1],
        started_at=started_at,
        completed_at=completed_at,
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
