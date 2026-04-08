from pydantic import BaseModel, Field
from typing import Optional, List


class JobEmailObservation(BaseModel):
    """What the agent sees at each step."""
    email_id: str = Field(description="Unique email identifier")
    subject: str = Field(description="Email subject line")
    body: str = Field(description="Email body text")
    sender: str = Field(description="Sender display name")
    sender_email: str = Field(description="Sender email address")
    sender_domain: str = Field(description="Domain portion of sender email")
    received_at: str = Field(description="ISO timestamp when email was received")
    has_attachment: bool = Field(description="Whether email has attachments")
    thread_length: int = Field(description="Number of messages in thread")
    task_id: str = Field(description="Current task identifier")
    step: int = Field(description="Current step number within episode")
    inbox_size: int = Field(description="Total emails remaining in inbox")
    candidate_profile: Optional[dict] = Field(
        default=None,
        description="Candidate profile for job matching (hard task only)"
    )


class JobEmailAction(BaseModel):
    """What the agent decides for each email."""
    category: str = Field(
        description=(
            "Email category: one of job_match | recruiter_outreach | "
            "application_update | job_alert_digest | promotional | deadline_alert"
        )
    )
    priority: str = Field(
        description="Priority level: one of urgent | high | normal | low"
    )
    action_required: str = Field(
        description=(
            "Action to take: one of reply | apply | archive | unsubscribe | flag | ignore"
        )
    )
    deadline_detected: Optional[str] = Field(
        default=None,
        description="Detected deadline date in YYYY-MM-DD format, if any"
    )
    reply_draft: Optional[str] = Field(
        default=None,
        description="Draft reply text (required for recruiter_outreach emails in hard task)"
    )
    reason: str = Field(
        description="Brief explanation of why this decision was made"
    )


class JobEmailReward(BaseModel):
    """Reward signal returned after each step."""
    value: float = Field(description="Reward value between 0.0 and 1.0")
    reason: str = Field(description="Human-readable explanation of reward")
    breakdown: dict = Field(
        default_factory=dict,
        description="Per-component score breakdown"
    )
