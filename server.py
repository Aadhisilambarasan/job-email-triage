"""
FastAPI server for the Job Email Triage OpenEnv environment.
Exposes: POST /reset, POST /step, GET /state, GET /health
"""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from env.environment import JobEmailTriageEnv
from env.models import JobEmailAction

app = FastAPI(
    title="Job Email Triage — OpenEnv",
    description=(
        "An AI environment that trains agents to triage a job seeker's inbox. "
        "Agents classify, prioritize, detect deadlines, and draft replies."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance (single session — suitable for evaluation)
_env = JobEmailTriageEnv()


# ─────────────────────────────────────────────
# REQUEST / RESPONSE MODELS
# ─────────────────────────────────────────────
class ResetRequest(BaseModel):
    task_id: Optional[str] = "easy_triage"


class StepRequest(BaseModel):
    action: JobEmailAction


# ─────────────────────────────────────────────
# ENDPOINTS
# ─────────────────────────────────────────────
@app.get("/")
@app.get("/health")
async def health():
    return {"status": "ok", "env": "job-email-triage", "version": "1.0.0"}


@app.post("/reset")
async def reset(req: ResetRequest = None):
    task_id = (req.task_id if req else None) or "easy_triage"
    try:
        obs = _env.reset(task_id=task_id)
        return {
            "observation": obs.dict(),
            "done": False,
            "info": {"task_id": task_id, "total_emails": len(_env.emails)},
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/step")
async def step(req: StepRequest):
    if not _env._initialized:
        raise HTTPException(status_code=400, detail="Call /reset first.")
    if _env.done:
        raise HTTPException(
            status_code=400,
            detail="Episode is done. Call /reset to start a new episode.",
        )
    try:
        result = _env.step(req.action)
        return result.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state")
async def state():
    return _env.state()


@app.get("/tasks")
async def list_tasks():
    return {
        "tasks": [
            {
                "id": "easy_triage",
                "name": "Easy — Spam vs Legitimate",
                "description": "Classify emails as spam or legitimate, assign priority.",
                "difficulty": "easy",
                "num_emails": 10,
            },
            {
                "id": "medium_triage",
                "name": "Medium — Full Categorization and Priority",
                "description": "Classify across 6 categories, assign priority and action.",
                "difficulty": "medium",
                "num_emails": 12,
            },
            {
                "id": "hard_triage",
                "name": "Hard — Full Pipeline",
                "description": (
                    "Full pipeline: categorize, prioritize, extract deadlines, "
                    "match against candidate profile, draft replies."
                ),
                "difficulty": "hard",
                "num_emails": 12,
            },
        ]
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
