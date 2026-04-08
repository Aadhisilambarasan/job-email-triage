"""
Task definitions and grader functions for the Job Email Triage environment.
Each grader returns a float in [0.0, 1.0].
"""

from typing import Dict, Any
from .models import JobEmailAction
from .data import EASY_EMAILS, MEDIUM_EMAILS, HARD_EMAILS, CANDIDATE_PROFILE


# ─────────────────────────────────────────────
# VALID VALUE SETS
# ─────────────────────────────────────────────
VALID_CATEGORIES = {
    "job_match", "recruiter_outreach", "application_update",
    "job_alert_digest", "promotional", "deadline_alert"
}
VALID_PRIORITIES = {"urgent", "high", "normal", "low"}
VALID_ACTIONS = {"reply", "apply", "archive", "unsubscribe", "flag", "ignore"}
SPAM_CATEGORIES = {"promotional"}
LEGIT_CATEGORIES = {
    "job_match", "recruiter_outreach", "application_update",
    "job_alert_digest", "deadline_alert"
}


# ─────────────────────────────────────────────
# TASK 1 GRADER — Easy (Spam vs Legit)
# ─────────────────────────────────────────────
def grade_easy(action: JobEmailAction, ground_truth: Dict[str, Any]) -> Dict[str, Any]:
    """
    Easy grader: rewards correctly identifying spam vs legitimate email
    and assigning the correct priority level.

    Scoring:
      - 0.60: correct spam/legit classification
      - 0.25: correct priority
      - 0.15: correct action_required
    """
    score = 0.0
    breakdown = {}

    # Check spam vs legit (most important signal)
    pred_is_spam = action.category in SPAM_CATEGORIES
    true_is_spam = ground_truth["is_spam"]
    if pred_is_spam == true_is_spam:
        score += 0.60
        breakdown["spam_detection"] = 0.60
    else:
        breakdown["spam_detection"] = 0.0
        # Heavy penalty: marking urgent email as spam
        if true_is_spam is False and ground_truth["priority"] == "urgent":
            score -= 0.20

    # Priority match
    if action.priority == ground_truth["priority"]:
        score += 0.25
        breakdown["priority"] = 0.25
    elif _priority_close(action.priority, ground_truth["priority"]):
        score += 0.10
        breakdown["priority"] = 0.10
    else:
        breakdown["priority"] = 0.0

    # Action match
    if action.action_required == ground_truth["action_required"]:
        score += 0.15
        breakdown["action"] = 0.15
    else:
        breakdown["action"] = 0.0

    final = max(0.0, min(1.0, score))
    return {"score": final, "breakdown": breakdown}


# ─────────────────────────────────────────────
# TASK 2 GRADER — Medium (Full Categorization)
# ─────────────────────────────────────────────
def grade_medium(action: JobEmailAction, ground_truth: Dict[str, Any]) -> Dict[str, Any]:
    """
    Medium grader: full 6-category classification + priority + action + deadline.

    Scoring:
      - 0.40: correct category
      - 0.25: correct priority
      - 0.20: correct action_required
      - 0.15: correct deadline detection (if applicable)
    """
    score = 0.0
    breakdown = {}

    # Category (hardest part — 6 classes)
    if action.category == ground_truth["category"]:
        score += 0.40
        breakdown["category"] = 0.40
    elif _category_adjacent(action.category, ground_truth["category"]):
        score += 0.15
        breakdown["category"] = 0.15
    else:
        breakdown["category"] = 0.0

    # Priority
    if action.priority == ground_truth["priority"]:
        score += 0.25
        breakdown["priority"] = 0.25
    elif _priority_close(action.priority, ground_truth["priority"]):
        score += 0.10
        breakdown["priority"] = 0.10
    else:
        breakdown["priority"] = 0.0

    # Action
    if action.action_required == ground_truth["action_required"]:
        score += 0.20
        breakdown["action"] = 0.20
    else:
        breakdown["action"] = 0.0

    # Deadline detection
    true_deadline = ground_truth.get("deadline_detected")
    if true_deadline:
        if action.deadline_detected and true_deadline in (action.deadline_detected or ""):
            score += 0.15
            breakdown["deadline"] = 0.15
        elif action.deadline_detected:
            score += 0.05  # detected something, wrong date
            breakdown["deadline"] = 0.05
        else:
            breakdown["deadline"] = 0.0
    else:
        # No deadline expected — reward for NOT hallucinating one
        if not action.deadline_detected:
            score += 0.15
            breakdown["deadline"] = 0.15
        else:
            score -= 0.05  # penalize hallucinated deadline
            breakdown["deadline"] = -0.05

    # Penalty: marking urgent as low
    if ground_truth["priority"] == "urgent" and action.priority == "low":
        score -= 0.20

    final = max(0.0, min(1.0, score))
    return {"score": final, "breakdown": breakdown}


# ─────────────────────────────────────────────
# TASK 3 GRADER — Hard (Full Pipeline)
# ─────────────────────────────────────────────
def grade_hard(action: JobEmailAction, ground_truth: Dict[str, Any]) -> Dict[str, Any]:
    """
    Hard grader: full pipeline with profile matching + reply drafting + deadline extraction.

    Scoring:
      - 0.25: correct category
      - 0.20: correct priority
      - 0.20: deadline extraction (if applicable)
      - 0.20: reply quality (if reply required)
      - 0.15: correct action_required / profile match decision

    Penalties:
      - -0.20: urgent email marked low
      - -0.15: reply drafted for non-reply email (wasted effort)
      - -0.10: deadline missed when clearly stated
    """
    score = 0.0
    breakdown = {}

    # Category
    if action.category == ground_truth["category"]:
        score += 0.25
        breakdown["category"] = 0.25
    elif _category_adjacent(action.category, ground_truth["category"]):
        score += 0.10
        breakdown["category"] = 0.10
    else:
        breakdown["category"] = 0.0

    # Priority
    if action.priority == ground_truth["priority"]:
        score += 0.20
        breakdown["priority"] = 0.20
    elif _priority_close(action.priority, ground_truth["priority"]):
        score += 0.08
        breakdown["priority"] = 0.08
    else:
        breakdown["priority"] = 0.0

    # Deadline extraction
    true_deadline = ground_truth.get("deadline_detected")
    if true_deadline:
        if action.deadline_detected and true_deadline in (action.deadline_detected or ""):
            score += 0.20
            breakdown["deadline"] = 0.20
        elif action.deadline_detected:
            score += 0.08
            breakdown["deadline"] = 0.08
        else:
            # Penalty for missing a stated deadline
            score -= 0.10
            breakdown["deadline"] = -0.10
    else:
        if not action.deadline_detected:
            score += 0.20
            breakdown["deadline"] = 0.20
        else:
            score -= 0.05
            breakdown["deadline"] = -0.05

    # Reply quality (for recruiter outreach emails that need replies)
    reply_required = ground_truth.get("reply_required", False)
    reply_keywords = ground_truth.get("reply_keywords", [])

    if reply_required:
        if action.reply_draft and len(action.reply_draft.strip()) > 30:
            draft_lower = action.reply_draft.lower()
            keyword_hits = sum(1 for kw in reply_keywords if kw.lower() in draft_lower)
            keyword_score = min(keyword_hits / max(len(reply_keywords), 1), 1.0)
            reply_score = 0.10 + (keyword_score * 0.10)
            score += reply_score
            breakdown["reply_quality"] = reply_score
        else:
            breakdown["reply_quality"] = 0.0
    else:
        # Penalize drafting replies for emails that don't need them
        if action.reply_draft and len(action.reply_draft.strip()) > 10:
            score -= 0.15
            breakdown["reply_quality"] = -0.15
        else:
            score += 0.20
            breakdown["reply_quality"] = 0.20

    # Action + profile match
    profile_match = ground_truth.get("profile_match", False)
    if action.action_required == ground_truth["action_required"]:
        score += 0.15
        breakdown["action"] = 0.15
    else:
        # Partial credit for correct profile-based decision
        if profile_match and action.action_required in {"reply", "apply", "flag"}:
            score += 0.07
            breakdown["action"] = 0.07
        elif not profile_match and action.action_required in {"archive", "ignore"}:
            score += 0.07
            breakdown["action"] = 0.07
        else:
            breakdown["action"] = 0.0

    # Hard penalties
    if ground_truth["priority"] == "urgent" and action.priority == "low":
        score -= 0.20
        breakdown["urgent_miss_penalty"] = -0.20

    final = max(0.0, min(1.0, score))
    return {"score": final, "breakdown": breakdown}


# ─────────────────────────────────────────────
# REWARD SHAPING (called by environment)
# ─────────────────────────────────────────────
def compute_shaped_reward(
    base_score: float,
    action: JobEmailAction,
    ground_truth: Dict[str, Any],
    step: int,
    total_steps: int,
) -> float:
    """
    Apply reward shaping on top of base grader score.
    Rewards catching urgent emails early; penalizes wasted effort on spam.
    """
    shaped = base_score

    # Bonus: catching urgent emails — earlier in episode is better
    if (ground_truth.get("priority") == "urgent"
            and action.priority == "urgent"):
        urgency_bonus = 0.05 * max(0, 1 - step / max(total_steps, 1))
        shaped += urgency_bonus

    # Small bonus: reason is non-empty and substantive
    if action.reason and len(action.reason.strip()) > 15:
        shaped += 0.02

    return max(0.0, min(1.0, shaped))


# ─────────────────────────────────────────────
# TASK REGISTRY
# ─────────────────────────────────────────────
TASKS = {
    "easy_triage": {
        "name": "Easy — Spam vs Legitimate",
        "emails": EASY_EMAILS,
        "grader": grade_easy,
    },
    "medium_triage": {
        "name": "Medium — Full Categorization and Priority",
        "emails": MEDIUM_EMAILS,
        "grader": grade_medium,
    },
    "hard_triage": {
        "name": "Hard — Full Pipeline with Profile Matching and Reply Drafting",
        "emails": HARD_EMAILS,
        "grader": grade_hard,
        "candidate_profile": CANDIDATE_PROFILE,
    },
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def _priority_close(pred: str, true: str) -> bool:
    """Returns True if priority is off by one level."""
    order = ["low", "normal", "high", "urgent"]
    if pred not in order or true not in order:
        return False
    return abs(order.index(pred) - order.index(true)) == 1


def _category_adjacent(pred: str, true: str) -> bool:
    """Returns True if categories are semantically close."""
    adjacency = {
        ("deadline_alert", "application_update"),
        ("application_update", "deadline_alert"),
        ("job_match", "job_alert_digest"),
        ("job_alert_digest", "job_match"),
        ("recruiter_outreach", "job_match"),
    }
    return (pred, true) in adjacency
