"""
inference.py — Baseline inference script for Job Email Triage OpenEnv environment.

Uses OpenAI client to run a language model against all 3 tasks and produces
reproducible baseline scores. Emits structured [START], [STEP], [END] logs.

Environment variables required:
  API_BASE_URL  — LLM API base URL
  MODEL_NAME    — Model identifier
  HF_TOKEN      — API key / HuggingFace token
  ENV_URL       — (optional) URL of the running environment server
"""

import os
import json
import asyncio
import httpx
from typing import List, Optional
from openai import OpenAI

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
API_BASE_URL: str = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME: str = os.environ.get("MODEL_NAME", "gpt-4o-mini")
API_KEY: str = os.environ.get("HF_TOKEN", os.environ.get("OPENAI_API_KEY", ""))
ENV_URL: str = os.environ.get("ENV_URL", "http://localhost:7860")

TEMPERATURE: float = 0.2
MAX_TOKENS: int = 512
MAX_STEPS: int = 15          # max emails per task
SUCCESS_SCORE_THRESHOLD: float = 0.60

TASKS = ["easy_triage", "medium_triage", "hard_triage"]
BENCHMARK = "job-email-triage"

# ─────────────────────────────────────────────
# SYSTEM PROMPT
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """You are an expert email triage assistant helping a job seeker manage their inbox.

For each email you receive, you must respond with a JSON object containing exactly these fields:
{
  "category": "<one of: job_match | recruiter_outreach | application_update | job_alert_digest | promotional | deadline_alert>",
  "priority": "<one of: urgent | high | normal | low>",
  "action_required": "<one of: reply | apply | archive | unsubscribe | flag | ignore>",
  "deadline_detected": "<YYYY-MM-DD if a deadline is mentioned, otherwise null>",
  "reply_draft": "<professional reply text if action is 'reply', otherwise null>",
  "reason": "<one sentence explaining your decision>"
}

Category definitions:
- job_match: A specific job posting recommended for the candidate
- recruiter_outreach: A human recruiter reaching out directly
- application_update: Status update on a submitted application (interview, rejection, shortlist, offer)
- job_alert_digest: Aggregated job alert digest (Indeed, Naukri, LinkedIn alerts with multiple jobs)
- promotional: Ads, course upsells, surveys, LinkedIn Premium offers, irrelevant marketing
- deadline_alert: Time-sensitive deadline (offer expiry, assignment due date, interview slot confirmation)

Priority definitions:
- urgent: Requires action within 24 hours (interview invite, offer deadline, assignment due)
- high: Strong opportunity or recruiter match worth responding to soon
- normal: Useful but not time-sensitive (application acknowledgement, digest to browse later)
- low: Promotional or irrelevant content

Respond ONLY with the JSON object. No preamble, no explanation outside the JSON."""


def build_user_prompt(obs: dict, step: int, task_id: str) -> str:
    profile_section = ""
    if obs.get("candidate_profile"):
        p = obs["candidate_profile"]
        profile_section = f"""
CANDIDATE PROFILE (use this to assess job match):
Name: {p.get('name')}
Role: {p.get('role')}
Skills: {', '.join(p.get('skills', []))}
Experience: {p.get('experience_years')} years
Preferred locations: {', '.join(p.get('preferred_location', []))}
Min salary (LPA): {p.get('min_salary_lpa')}
Preferred domains: {', '.join(p.get('preferred_domains', []))}
Open to contract: {p.get('open_to_contract')}
"""

    return f"""TASK: {task_id} | Step {step} | Inbox size: {obs.get('inbox_size', 0)} remaining
{profile_section}
EMAIL TO TRIAGE:
From: {obs.get('sender')} <{obs.get('sender_email')}>
Subject: {obs.get('subject')}
Received: {obs.get('received_at')}
Has attachment: {obs.get('has_attachment')}
Thread length: {obs.get('thread_length')} message(s)

Body:
{obs.get('body')}

Respond with the JSON triage decision:"""


# ─────────────────────────────────────────────
# STRUCTURED LOG HELPERS (mandatory format)
# ─────────────────────────────────────────────
def log_start(task: str, env: str, model: str) -> None:
    print(json.dumps({
        "event": "START",
        "task": task,
        "env": env,
        "model": model,
    }), flush=True)


def log_step(step: int, action: dict, reward: float, done: bool, error: Optional[str]) -> None:
    print(json.dumps({
        "event": "STEP",
        "step": step,
        "action": action,
        "reward": reward,
        "done": done,
        "error": error,
    }), flush=True)


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    print(json.dumps({
        "event": "END",
        "success": success,
        "steps": steps,
        "score": score,
        "rewards": rewards,
    }), flush=True)


# ─────────────────────────────────────────────
# MODEL CALL
# ─────────────────────────────────────────────
def get_model_action(client: OpenAI, obs: dict, step: int, task_id: str) -> dict:
    user_prompt = build_user_prompt(obs, step, task_id)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        action_dict = json.loads(text)
        return action_dict
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return {
            "category": "promotional",
            "priority": "normal",
            "action_required": "archive",
            "deadline_detected": None,
            "reply_draft": None,
            "reason": "fallback due to model error",
        }


# ─────────────────────────────────────────────
# ENVIRONMENT HTTP CLIENT
# ─────────────────────────────────────────────
class EnvClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=30.0)

    def reset(self, task_id: str) -> dict:
        r = self.client.post(
            f"{self.base_url}/reset",
            json={"task_id": task_id}
        )
        r.raise_for_status()
        return r.json()

    def step(self, action: dict) -> dict:
        r = self.client.post(
            f"{self.base_url}/step",
            json={"action": action}
        )
        r.raise_for_status()
        return r.json()

    def state(self) -> dict:
        r = self.client.get(f"{self.base_url}/state")
        r.raise_for_status()
        return r.json()

    def close(self):
        self.client.close()


# ─────────────────────────────────────────────
# RUN SINGLE TASK
# ─────────────────────────────────────────────
def run_task(
    openai_client: OpenAI,
    env_client: EnvClient,
    task_id: str,
) -> float:
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_id, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = env_client.reset(task_id=task_id)
        obs = result["observation"]
        done = result.get("done", False)
        total_emails = result.get("info", {}).get("total_emails", MAX_STEPS)
        max_total_reward = float(total_emails)

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            action_dict = get_model_action(openai_client, obs, step, task_id)

            try:
                step_result = env_client.step(action_dict)
            except Exception as e:
                log_step(step=step, action=action_dict, reward=0.0, done=True, error=str(e))
                break

            obs = step_result["observation"]
            reward = float(step_result.get("reward") or 0.0)
            done = step_result.get("done", False)
            error = None

            rewards.append(reward)
            steps_taken = step

            log_step(step=step, action=action_dict, reward=reward, done=done, error=error)

            if done:
                break

        score = sum(rewards) / max_total_reward if max_total_reward > 0 else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Task {task_id} failed: {e}", flush=True)

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

    return score


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main() -> None:
    print(f"[DEBUG] Starting inference: model={MODEL_NAME} env={ENV_URL}", flush=True)

    openai_client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    env_client = EnvClient(base_url=ENV_URL)

    all_scores = {}

    try:
        for task_id in TASKS:
            print(f"\n[DEBUG] ===== Running task: {task_id} =====", flush=True)
            score = run_task(openai_client, env_client, task_id)
            all_scores[task_id] = score
            print(f"[DEBUG] Task {task_id} score: {score:.4f}", flush=True)

    finally:
        env_client.close()

    # Final summary
    avg_score = sum(all_scores.values()) / len(all_scores) if all_scores else 0.0
    print("\n" + "=" * 50, flush=True)
    print("BASELINE RESULTS:", flush=True)
    for task_id, score in all_scores.items():
        print(f"  {task_id}: {score:.4f}", flush=True)
    print(f"  AVERAGE: {avg_score:.4f}", flush=True)
    print("=" * 50, flush=True)


if __name__ == "__main__":
    main()
