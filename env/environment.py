"""
Job Email Triage Environment — main environment class.
Implements the OpenEnv interface: reset(), step(), state().
"""

import copy
from typing import Optional, Dict, Any

from .models import JobEmailObservation, JobEmailAction, JobEmailReward
from .tasks import TASKS, compute_shaped_reward


class StepResult:
    def __init__(
        self,
        observation: JobEmailObservation,
        reward: float,
        done: bool,
        info: Dict[str, Any],
    ):
        self.observation = observation
        self.reward = reward
        self.done = done
        self.info = info

    def dict(self):
        return {
            "observation": self.observation.dict(),
            "reward": self.reward,
            "done": self.done,
            "info": self.info,
        }


class JobEmailTriageEnv:
    """
    Job Email Triage Environment.

    An AI agent triage's a job seeker's inbox across 3 tasks of increasing
    difficulty: spam detection, full categorization, and full pipeline with
    deadline extraction and reply drafting.
    """

    def __init__(self):
        self.task_id: str = "easy_triage"
        self.task: Optional[Dict] = None
        self.emails: list = []
        self.step_num: int = 0
        self.current_email: Optional[Dict] = None
        self.episode_rewards: list = []
        self.done: bool = False
        self._initialized: bool = False

    # ─────────────────────────────────────────────
    # RESET
    # ─────────────────────────────────────────────
    def reset(self, task_id: str = "easy_triage") -> JobEmailObservation:
        """
        Reset the environment for a new episode.
        Returns the first observation.
        """
        if task_id not in TASKS:
            raise ValueError(
                f"Unknown task_id: {task_id!r}. "
                f"Valid tasks: {list(TASKS.keys())}"
            )

        self.task_id = task_id
        self.task = TASKS[task_id]
        self.emails = copy.deepcopy(self.task["emails"])
        self.step_num = 0
        self.episode_rewards = []
        self.done = False
        self._initialized = True

        self.current_email = self.emails[0]
        return self._make_observation()

    # ─────────────────────────────────────────────
    # STEP
    # ─────────────────────────────────────────────
    def step(self, action: JobEmailAction) -> StepResult:
        """
        Process agent action for current email.
        Returns next observation, reward, done flag, and info dict.
        """
        if not self._initialized:
            raise RuntimeError("Environment not initialized. Call reset() first.")
        if self.done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")

        # Validate action fields
        action = self._validate_action(action)

        # Grade the action
        ground_truth = self.current_email["ground_truth"]
        grader = self.task["grader"]
        result = grader(action, ground_truth)
        base_score = result["score"]
        breakdown = result["breakdown"]

        # Apply reward shaping
        total_steps = len(self.emails)
        shaped_reward = compute_shaped_reward(
            base_score, action, ground_truth, self.step_num, total_steps
        )

        self.episode_rewards.append(shaped_reward)

        # Advance to next email
        self.step_num += 1
        done = self.step_num >= len(self.emails)
        self.done = done

        if not done:
            self.current_email = self.emails[self.step_num]
            obs = self._make_observation()
        else:
            obs = self._make_observation()  # return last email obs with done=True

        info = {
            "email_id": self.current_email["email_id"],
            "ground_truth": ground_truth,
            "breakdown": breakdown,
            "base_score": base_score,
            "shaped_reward": shaped_reward,
            "episode_step": self.step_num,
            "total_emails": len(self.emails),
            "cumulative_reward": sum(self.episode_rewards),
        }

        return StepResult(
            observation=obs,
            reward=shaped_reward,
            done=done,
            info=info,
        )

    # ─────────────────────────────────────────────
    # STATE
    # ─────────────────────────────────────────────
    def state(self) -> Dict[str, Any]:
        """Returns current environment state."""
        return {
            "task_id": self.task_id,
            "step": self.step_num,
            "total_emails": len(self.emails) if self.emails else 0,
            "done": self.done,
            "initialized": self._initialized,
            "episode_rewards": self.episode_rewards,
            "cumulative_reward": sum(self.episode_rewards) if self.episode_rewards else 0.0,
            "current_email_id": (
                self.current_email["email_id"] if self.current_email else None
            ),
        }

    # ─────────────────────────────────────────────
    # INTERNAL HELPERS
    # ─────────────────────────────────────────────
    def _make_observation(self) -> JobEmailObservation:
        email = self.current_email
        candidate_profile = self.task.get("candidate_profile") if self.task else None
        return JobEmailObservation(
            email_id=email["email_id"],
            subject=email["subject"],
            body=email["body"],
            sender=email["sender"],
            sender_email=email["sender_email"],
            sender_domain=email["sender_domain"],
            received_at=email["received_at"],
            has_attachment=email["has_attachment"],
            thread_length=email["thread_length"],
            task_id=self.task_id,
            step=self.step_num,
            inbox_size=max(0, len(self.emails) - self.step_num),
            candidate_profile=candidate_profile,
        )

    def _validate_action(self, action: JobEmailAction) -> JobEmailAction:
        """Normalize action fields to lowercase and valid values."""
        valid_categories = {
            "job_match", "recruiter_outreach", "application_update",
            "job_alert_digest", "promotional", "deadline_alert"
        }
        valid_priorities = {"urgent", "high", "normal", "low"}
        valid_actions = {"reply", "apply", "archive", "unsubscribe", "flag", "ignore"}

        cat = (action.category or "").lower().strip()
        pri = (action.priority or "").lower().strip()
        act = (action.action_required or "").lower().strip()

        return JobEmailAction(
            category=cat if cat in valid_categories else "promotional",
            priority=pri if pri in valid_priorities else "normal",
            action_required=act if act in valid_actions else "archive",
            deadline_detected=action.deadline_detected,
            reply_draft=action.reply_draft,
            reason=action.reason or "",
        )
