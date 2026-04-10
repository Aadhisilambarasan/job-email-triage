---
title: Job Email Triage OpenEnv
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1"
python_version: "3.10"
app_port: 7860
pinned: false
---

# Job Email Triage OpenEnv Environment

> An AI environment that trains agents to handle the overwhelming inbox of an active job seeker.

[![OpenEnv](https://img.shields.io/badge/OpenEnv-compatible-blue)](https://openenv.dev)
[![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace%20Space-yellow)](https://huggingface.co/spaces)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-green)](https://python.org)

---

## 🎯 Problem & Motivation

An active job seeker receives **80–150 emails per day** — a mix of interview invites buried under LinkedIn Premium ads, recruiter spam disguised as opportunities, offer deadlines hidden in digest threads, and rejection emails that still need archiving.

**Missing a single interview invite or offer deadline can cost real career opportunities.**

This environment trains and evaluates AI agents that act as a personal job search assistant — triaging the inbox so the job seeker only sees what matters, when it matters.

**Real-world impact of a well-trained agent (scoring ≥ 0.8 on Task 3):**
- ✅ Surface interview invites within seconds of arrival
- ✅ Draft professional recruiter replies automatically
- ✅ Never miss application deadlines
- ✅ Match job postings against the candidate's actual skill profile
- ✅ Unsubscribe from noise automatically

---

## 🏗️ Environment Architecture

```
job-email-triage/
├── env/
│   ├── environment.py   # JobEmailTriageEnv — step/reset/state
│   ├── models.py        # Pydantic: Observation, Action, Reward
│   ├── tasks.py         # 3 tasks + graders + reward shaping
│   └── data.py          # 34 realistic emails with ground truth
├── server.py            # FastAPI HTTP server (OpenEnv endpoints)
├── inference.py         # Baseline inference script
├── openenv.yaml         # OpenEnv spec metadata
├── Dockerfile           # Container for HF Spaces
├── requirements.txt
└── README.md
```

---

## 📐 Observation Space

What the agent sees at each step:

| Field | Type | Description |
|---|---|---|
| `email_id` | str | Unique email identifier |
| `subject` | str | Email subject line |
| `body` | str | Full email body |
| `sender` | str | Sender display name |
| `sender_email` | str | Full sender email address |
| `sender_domain` | str | Domain (e.g., `linkedin.com`, `promo-spam.xyz`) |
| `received_at` | str | ISO 8601 timestamp |
| `has_attachment` | bool | Whether attachments are present |
| `thread_length` | int | Messages in thread (context signal) |
| `task_id` | str | Which task is running |
| `step` | int | Current step number |
| `inbox_size` | int | Emails remaining in inbox |
| `candidate_profile` | dict\|null | Candidate profile for job matching (hard task only) |

---

## 🎮 Action Space

What the agent decides per email:

| Field | Type | Valid Values | Description |
|---|---|---|---|
| `category` | str | `job_match`, `recruiter_outreach`, `application_update`, `job_alert_digest`, `promotional`, `deadline_alert` | Email classification |
| `priority` | str | `urgent`, `high`, `normal`, `low` | Priority assignment |
| `action_required` | str | `reply`, `apply`, `archive`, `unsubscribe`, `flag`, `ignore` | Action to take |
| `deadline_detected` | str\|null | `YYYY-MM-DD` | Extracted deadline date if present |
| `reply_draft` | str\|null | Any text | Professional reply draft (for recruiter/urgent emails) |
| `reason` | str | Any text | Brief explanation of the triage decision |

---

## 📊 Tasks

### Task 1 — Easy: Spam vs Legitimate
**Goal:** Identify whether each email is spam/promotional or a legitimate job-related email. Assign a basic priority level.

**Grader scoring:**
- 0.60 — Correct spam vs legitimate classification
- 0.25 — Correct priority level
- 0.15 — Correct action required

**Penalty:** -0.20 if an urgent email is misclassified as spam.

**Expected scores:** Random ~0.25 | GPT-4o-mini ~0.82 | GPT-4o ~0.93

---

### Task 2 — Medium: Full Categorization and Priority
**Goal:** Classify emails across all 6 categories, assign priority, choose the correct action, and detect deadlines where present.

**Grader scoring:**
- 0.40 — Correct 6-class category
- 0.25 — Correct priority
- 0.20 — Correct action
- 0.15 — Correct deadline detection / no hallucinated deadline

**Penalty:** -0.20 if urgent email marked as low priority.

**Expected scores:** Random ~0.12 | GPT-4o-mini ~0.62 | GPT-4o ~0.76

---

### Task 3 — Hard: Full Pipeline with Profile Matching and Reply Drafting
**Goal:** Full triage pipeline. Agent must categorize, prioritize, extract deadlines, match job descriptions against the candidate's profile, and draft professional replies for recruiter emails — while penalized for unnecessary replies to spam.

**Grader scoring:**
- 0.25 — Correct category
- 0.20 — Correct priority
- 0.20 — Deadline extraction (penalty -0.10 for missing a stated deadline)
- 0.20 — Reply quality: keyword coverage + length (penalty -0.15 for replying to spam)
- 0.15 — Correct action / profile match decision

**Penalty:** -0.20 if urgent email marked low, -0.15 if reply drafted for non-reply email.

**Expected scores:** Random ~0.08 | GPT-4o-mini ~0.45 | GPT-4o ~0.58

---

## 🏆 Reward Function

### Base reward
Each step returns a reward `∈ [0.0, 1.0]` from the task-specific grader.

### Reward shaping
```python
# Urgency bonus — catching urgent emails early matters most
if ground_truth["priority"] == "urgent" and action.priority == "urgent":
    urgency_bonus = 0.05 * (1 - step / total_steps)
    reward += urgency_bonus

# Small bonus for providing a meaningful reason
if len(action.reason.strip()) > 15:
    reward += 0.02
```

### Penalties (baked into graders)
- `-0.20` — marking urgent email as low priority
- `-0.15` — drafting a reply for a spam/promotional email
- `-0.10` — missing a deadline that was explicitly stated in the email body
- `-0.05` — hallucinating a deadline when none exists

The reward function provides **dense signal across the full trajectory** — not just binary end-of-episode reward — enabling effective RL training.

---

## 🔌 API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/reset` | Start new episode `{"task_id": "easy_triage"}` |
| POST | `/step` | Submit action `{"action": {...}}` |
| GET | `/state` | Current environment state |
| GET | `/tasks` | List all available tasks |

---

## 🚀 Setup & Usage

### Local development

```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/job-email-triage
cd job-email-triage
pip install -r requirements.txt
python server.py
```

Server starts at `http://localhost:7860`.

### Docker

```bash
docker build -t job-email-triage .
docker run -p 7860:7860 job-email-triage
```

### Run inference baseline

```bash
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-4o-mini"
export HF_TOKEN="your-api-key"
export ENV_URL="http://localhost:7860"

python inference.py
```

---

## 📈 Baseline Scores

Run with `gpt-4o-mini` (temperature=0.2):

| Task | Score | Notes |
|---|---|---|
| easy_triage | ~0.82 | Spam detection is reliable |
| medium_triage | ~0.62 | 6-class confusion on adjacent categories |
| hard_triage | ~0.45 | Deadline extraction + reply drafting challenges |
| **Average** | **~0.63** | |

---

## 🧪 Quick Test (curl)

```bash
# Reset to easy task
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy_triage"}'

# Submit a triage decision
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "action": {
      "category": "promotional",
      "priority": "low",
      "action_required": "unsubscribe",
      "deadline_detected": null,
      "reply_draft": null,
      "reason": "LinkedIn Premium upsell — classic promotional spam"
    }
  }'
```

---

## 📄 License

MIT — open for research and evaluation use.
