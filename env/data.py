"""
Realistic email dataset for the Job Email Triage environment.
Each email has ground truth labels for grading agent responses.
"""

CANDIDATE_PROFILE = {
    "name": "Alex Johnson",
    "role": "Senior Software Engineer",
    "skills": ["Python", "FastAPI", "PostgreSQL", "AWS", "Docker", "Kubernetes"],
    "experience_years": 6,
    "preferred_location": ["Remote", "Bangalore", "Hyderabad"],
    "min_salary_lpa": 25,
    "preferred_domains": ["FinTech", "SaaS", "AI/ML"],
    "open_to_contract": False,
}

# ─────────────────────────────────────────────
# TASK 1: EASY — Spam vs Legitimate (10 emails)
# Agent only needs to detect promo vs legit + basic priority
# ─────────────────────────────────────────────
EASY_EMAILS = [
    {
        "email_id": "easy_001",
        "subject": "Interview Scheduled: Senior Engineer @ FinEdge Technologies",
        "body": (
            "Dear Alex,\n\nThank you for applying to FinEdge Technologies. "
            "We are pleased to invite you for a technical interview on Thursday, "
            "April 11th at 10:30 AM IST via Google Meet.\n\n"
            "Please confirm your availability by replying to this email.\n\n"
            "Best regards,\nPriya Sharma\nTalent Acquisition, FinEdge Technologies"
        ),
        "sender": "Priya Sharma",
        "sender_email": "priya.sharma@finedge.io",
        "sender_domain": "finedge.io",
        "received_at": "2026-04-08T09:15:00Z",
        "has_attachment": False,
        "thread_length": 2,
        "ground_truth": {
            "category": "application_update",
            "priority": "urgent",
            "action_required": "reply",
            "deadline_detected": "2026-04-11",
            "is_spam": False,
        },
    },
    {
        "email_id": "easy_002",
        "subject": "🔥 LIMITED TIME: Upgrade to LinkedIn Premium — 50% OFF Today Only!",
        "body": (
            "Hi there,\n\nDon't miss out! For the next 24 hours only, "
            "LinkedIn Premium is available at 50% off. Get InMail credits, "
            "see who viewed your profile, and stand out to recruiters!\n\n"
            "Click here to claim your discount: [LINK]\n\n"
            "Offer expires midnight. Act now!\n\nTeam LinkedIn"
        ),
        "sender": "LinkedIn Premium",
        "sender_email": "offers@e.linkedin-promo.com",
        "sender_domain": "linkedin-promo.com",
        "received_at": "2026-04-08T07:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "promotional",
            "priority": "low",
            "action_required": "unsubscribe",
            "deadline_detected": None,
            "is_spam": True,
        },
    },
    {
        "email_id": "easy_003",
        "subject": "Your application was received — Backend Engineer at CloudNova",
        "body": (
            "Hi Alex,\n\nThank you for applying to the Backend Engineer position at CloudNova. "
            "We have received your application and our team will review it shortly. "
            "You can expect to hear back within 5-7 business days.\n\n"
            "Best,\nCloudNova Recruiting Team"
        ),
        "sender": "CloudNova Recruiting",
        "sender_email": "no-reply@cloudnova.com",
        "sender_domain": "cloudnova.com",
        "received_at": "2026-04-07T14:20:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "application_update",
            "priority": "normal",
            "action_required": "archive",
            "deadline_detected": None,
            "is_spam": False,
        },
    },
    {
        "email_id": "easy_004",
        "subject": "Earn your AWS Certification in 4 weeks — Enroll Now!",
        "body": (
            "Hello,\n\nBoost your career with our AWS Solutions Architect course! "
            "Join 50,000+ professionals who certified with us. "
            "Limited seats available — enroll by Sunday for the early bird discount.\n\n"
            "Use code CLOUD30 for 30% off.\n\nSkillUp Academy"
        ),
        "sender": "SkillUp Academy",
        "sender_email": "promo@skillupacademy.io",
        "sender_domain": "skillupacademy.io",
        "received_at": "2026-04-08T06:45:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "promotional",
            "priority": "low",
            "action_required": "unsubscribe",
            "deadline_detected": None,
            "is_spam": True,
        },
    },
    {
        "email_id": "easy_005",
        "subject": "Hi Alex — Open to a Senior Python role at a stealth FinTech?",
        "body": (
            "Hi Alex,\n\nI came across your profile on LinkedIn and was impressed "
            "by your work with FastAPI and PostgreSQL. I'm working with a stealth-mode "
            "FinTech startup (Series B, 120 people) looking for a Senior Python Engineer.\n\n"
            "Comp: ₹32–38 LPA + ESOPs. Fully remote.\n\n"
            "Would love to set up a quick 15-minute call this week. Are you open?\n\n"
            "Cheers,\nRahul Mehta\nTech Recruiter"
        ),
        "sender": "Rahul Mehta",
        "sender_email": "rahul.mehta@talentbridge.in",
        "sender_domain": "talentbridge.in",
        "received_at": "2026-04-08T10:30:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "high",
            "action_required": "reply",
            "deadline_detected": None,
            "is_spam": False,
        },
    },
    {
        "email_id": "easy_006",
        "subject": "We regret to inform you — Software Engineer @ DataPulse",
        "body": (
            "Dear Alex,\n\nThank you for your interest in the Software Engineer role at DataPulse. "
            "After careful consideration, we have decided to move forward with other candidates "
            "whose experience more closely matches our current needs.\n\n"
            "We encourage you to apply for future openings.\n\n"
            "Best regards,\nDataPulse HR Team"
        ),
        "sender": "DataPulse HR",
        "sender_email": "hr@datapulse.ai",
        "sender_domain": "datapulse.ai",
        "received_at": "2026-04-07T16:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "application_update",
            "priority": "normal",
            "action_required": "archive",
            "deadline_detected": None,
            "is_spam": False,
        },
    },
    {
        "email_id": "easy_007",
        "subject": "🎯 47 new jobs matching 'Python Developer' — Indeed Job Alert",
        "body": (
            "Your daily job alert from Indeed\n\n"
            "47 new jobs matching Python Developer in Bangalore\n\n"
            "• Senior Python Developer — TechCorp (₹20-28 LPA)\n"
            "• Python Backend Engineer — Razorpay (₹25-35 LPA)\n"
            "• Python Developer — Infosys (₹8-14 LPA)\n"
            "• ... and 44 more\n\n"
            "View all jobs → [LINK]\n\nIndeed Job Alerts"
        ),
        "sender": "Indeed Job Alerts",
        "sender_email": "jobalert@indeed.com",
        "sender_domain": "indeed.com",
        "received_at": "2026-04-08T08:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "job_alert_digest",
            "priority": "normal",
            "action_required": "archive",
            "deadline_detected": None,
            "is_spam": False,
        },
    },
    {
        "email_id": "easy_008",
        "subject": "URGENT: Final reminder — offer expires in 24 hours",
        "body": (
            "Dear Alex,\n\nThis is a final reminder that your job offer from "
            "NexGen Solutions expires TOMORROW at 5 PM IST. Please sign and "
            "return the offer letter by then to confirm your acceptance.\n\n"
            "Attached: Offer_Letter_Alex_Johnson.pdf\n\n"
            "Reach out if you have questions.\n\nAnanya Kapoor\nHR Lead, NexGen Solutions"
        ),
        "sender": "Ananya Kapoor",
        "sender_email": "ananya.k@nexgensolutions.com",
        "sender_domain": "nexgensolutions.com",
        "received_at": "2026-04-08T11:00:00Z",
        "has_attachment": True,
        "thread_length": 3,
        "ground_truth": {
            "category": "deadline_alert",
            "priority": "urgent",
            "action_required": "reply",
            "deadline_detected": "2026-04-09",
            "is_spam": False,
        },
    },
    {
        "email_id": "easy_009",
        "subject": "Take our 2-minute salary survey — Win a ₹5000 Amazon voucher",
        "body": (
            "Hi Tech Professional,\n\nHelp us understand tech salaries in India! "
            "Complete our 2-minute survey and get a chance to win ₹5000 Amazon Gift Card.\n\n"
            "Survey link: [LINK]\n\nJobsDB Research Team"
        ),
        "sender": "JobsDB Research",
        "sender_email": "survey@jobsdb-research.com",
        "sender_domain": "jobsdb-research.com",
        "received_at": "2026-04-07T13:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "promotional",
            "priority": "low",
            "action_required": "ignore",
            "deadline_detected": None,
            "is_spam": True,
        },
    },
    {
        "email_id": "easy_010",
        "subject": "New job recommendation: Staff Engineer @ Stripe India",
        "body": (
            "Hi Alex,\n\nBased on your profile, we think you'd be a great fit for:\n\n"
            "Staff Engineer — Stripe India\n"
            "📍 Remote (India) | 💰 ₹45-60 LPA | 🏢 Stripe\n\n"
            "Requirements: 8+ years backend, distributed systems, payments domain.\n\n"
            "Apply now → [LINK]\n\nLinkedIn Jobs"
        ),
        "sender": "LinkedIn Jobs",
        "sender_email": "jobs-noreply@linkedin.com",
        "sender_domain": "linkedin.com",
        "received_at": "2026-04-08T09:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "job_match",
            "priority": "high",
            "action_required": "apply",
            "deadline_detected": None,
            "is_spam": False,
        },
    },
]

# ─────────────────────────────────────────────
# TASK 2: MEDIUM — Full Categorization + Priority (12 emails)
# Agent must correctly classify all 6 categories + priority + action
# ─────────────────────────────────────────────
MEDIUM_EMAILS = [
    {
        "email_id": "med_001",
        "subject": "Technical Interview — Round 2 at Groww (confirm by Thursday)",
        "body": (
            "Hi Alex,\n\nCongratulations on clearing Round 1!\n\n"
            "We'd like to schedule your Round 2 System Design interview at Groww. "
            "Available slots: Thursday April 10th (2PM or 4PM IST) or Friday April 11th (11AM IST).\n\n"
            "Please confirm your preferred slot by Thursday morning.\n\n"
            "Best,\nSandeep Nair\nEngineering Hiring, Groww"
        ),
        "sender": "Sandeep Nair",
        "sender_email": "sandeep.nair@groww.in",
        "sender_domain": "groww.in",
        "received_at": "2026-04-08T10:00:00Z",
        "has_attachment": False,
        "thread_length": 3,
        "ground_truth": {
            "category": "deadline_alert",
            "priority": "urgent",
            "action_required": "reply",
            "deadline_detected": "2026-04-10",
        },
    },
    {
        "email_id": "med_002",
        "subject": "RE: Your application — Backend Engineer at ClearTax",
        "body": (
            "Hi Alex,\n\nWe've reviewed your profile and believe you could be a strong fit "
            "for our Backend Engineer role. We'd love to start with a quick 20-minute "
            "screening call.\n\nAre you available this week or next?\n\n"
            "Regards,\nMeghna Pillai\nTalent Team, ClearTax"
        ),
        "sender": "Meghna Pillai",
        "sender_email": "meghna@cleartax.in",
        "sender_domain": "cleartax.in",
        "received_at": "2026-04-07T15:30:00Z",
        "has_attachment": False,
        "thread_length": 2,
        "ground_truth": {
            "category": "application_update",
            "priority": "high",
            "action_required": "reply",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_003",
        "subject": "🚀 65 new Python jobs in Bangalore — Naukri Job Alert",
        "body": (
            "Your Naukri Job Alert — Python Developer, Bangalore\n\n"
            "65 new jobs posted today:\n"
            "• Python Developer — Infosys BPM (3-5 yrs, ₹10-15 LPA)\n"
            "• Sr. Python Engineer — PhonePe (5-8 yrs, ₹28-40 LPA)\n"
            "• Python Full Stack — Wipro (2-4 yrs, ₹8-12 LPA)\n"
            "• ... 62 more jobs\n\n"
            "View all → naukri.com/jobsearch\n\nNaukri.com"
        ),
        "sender": "Naukri Job Alert",
        "sender_email": "jobalert@naukri.com",
        "sender_domain": "naukri.com",
        "received_at": "2026-04-08T07:30:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "job_alert_digest",
            "priority": "normal",
            "action_required": "archive",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_004",
        "subject": "Exciting Senior SDE-II opportunity at Zepto — Interested?",
        "body": (
            "Hi Alex,\n\nI hope you're doing well! I'm a recruiter at Talent Nexus "
            "and I'm working with Zepto on an urgent hiring need for Senior SDE-II.\n\n"
            "Role: Senior SDE-II — Backend\n"
            "Stack: Python, Go, Kafka, Redis\n"
            "Comp: ₹35-42 LPA + ESOPs\n"
            "Location: Remote-first\n\n"
            "This is an urgent position — they're looking to close by end of April. "
            "Would you be open to a brief conversation?\n\n"
            "Thanks,\nKiran Desai\nSenior Recruiter, Talent Nexus"
        ),
        "sender": "Kiran Desai",
        "sender_email": "kiran.desai@talentnexus.in",
        "sender_domain": "talentnexus.in",
        "received_at": "2026-04-08T09:45:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "high",
            "action_required": "reply",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_005",
        "subject": "Master System Design — Join 12,000+ engineers — Enroll by Sunday",
        "body": (
            "Hi Alex,\n\nOur System Design Masterclass has helped 12,000+ engineers "
            "crack FAANG interviews. Taught by ex-Google, ex-Amazon engineers.\n\n"
            "🎯 Next batch starts April 14th\n"
            "💰 ₹8,999 (Early Bird — ends Sunday)\n\n"
            "Enroll now → [LINK]\n\nInterviewReady Team"
        ),
        "sender": "InterviewReady",
        "sender_email": "courses@interviewready.io",
        "sender_domain": "interviewready.io",
        "received_at": "2026-04-08T08:15:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "promotional",
            "priority": "low",
            "action_required": "unsubscribe",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_006",
        "subject": "Application Update: You've been shortlisted — CRED Engineering",
        "body": (
            "Dear Alex,\n\nGreat news! Your profile has been shortlisted for the "
            "Senior Backend Engineer position at CRED.\n\n"
            "Next step: We'll be sending you a take-home assignment within 48 hours. "
            "You will have 72 hours to complete it once received.\n\n"
            "Please ensure your contact details are up to date.\n\n"
            "Warm regards,\nCRED Talent Team"
        ),
        "sender": "CRED Talent Team",
        "sender_email": "talent@cred.club",
        "sender_domain": "cred.club",
        "received_at": "2026-04-07T17:00:00Z",
        "has_attachment": False,
        "thread_length": 2,
        "ground_truth": {
            "category": "application_update",
            "priority": "high",
            "action_required": "flag",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_007",
        "subject": "Job opportunity: Senior Python Developer at FinTech Startup",
        "body": (
            "Hi,\n\nI'm reaching out from BuildFast Consulting. Our client, "
            "a growing FinTech startup, is urgently looking for a Senior Python Developer.\n\n"
            "Budget: ₹40-50 LPA\nMode: Remote\nNotice: Immediate to 30 days preferred\n\n"
            "Please share your updated CV and we'll set up a call.\n\n"
            "Thanks,\nRecruitment Team\nBuildFast Consulting"
        ),
        "sender": "Recruitment Team",
        "sender_email": "recruit@buildfastconsulting.com",
        "sender_domain": "buildfastconsulting.com",
        "received_at": "2026-04-08T11:30:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "high",
            "action_required": "reply",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_008",
        "subject": "REMINDER: Complete your Razorpay assignment — due in 12 hours",
        "body": (
            "Hi Alex,\n\nThis is a reminder that your take-home assignment for "
            "the Senior Engineer role at Razorpay is due in 12 hours (April 9, 11:59 PM IST).\n\n"
            "Submission portal: [LINK]\n\n"
            "Please submit on time — late submissions will not be reviewed.\n\n"
            "Good luck!\nRazorpay Engineering Team"
        ),
        "sender": "Razorpay Engineering",
        "sender_email": "engineering-hiring@razorpay.com",
        "sender_domain": "razorpay.com",
        "received_at": "2026-04-08T12:00:00Z",
        "has_attachment": False,
        "thread_length": 2,
        "ground_truth": {
            "category": "deadline_alert",
            "priority": "urgent",
            "action_required": "flag",
            "deadline_detected": "2026-04-09",
        },
    },
    {
        "email_id": "med_009",
        "subject": "Your profile views increased 340% this week — Here's why",
        "body": (
            "Hi Alex,\n\nYour LinkedIn profile was viewed 340% more than usual this week! "
            "To get even more visibility, upgrade to LinkedIn Premium and see exactly "
            "who's viewing your profile.\n\nStart your free 1-month trial → [LINK]\n\n"
            "LinkedIn"
        ),
        "sender": "LinkedIn",
        "sender_email": "notifications@linkedin.com",
        "sender_domain": "linkedin.com",
        "received_at": "2026-04-08T07:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "promotional",
            "priority": "low",
            "action_required": "ignore",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_010",
        "subject": "New job: Staff Engineer — Anthropic India (Remote, ₹55-80 LPA)",
        "body": (
            "Hi Alex,\n\nA new job matching your profile:\n\n"
            "Staff Engineer, India — Anthropic\n"
            "📍 Remote (India) | 💰 ₹55-80 LPA\n"
            "Requirements: 8+ years, Python, distributed systems, ML infra experience.\n\n"
            "Apply → [LINK]\n\nLinkedIn Jobs"
        ),
        "sender": "LinkedIn Jobs",
        "sender_email": "jobs-noreply@linkedin.com",
        "sender_domain": "linkedin.com",
        "received_at": "2026-04-08T09:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "job_match",
            "priority": "high",
            "action_required": "apply",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_011",
        "subject": "Thank you for attending our webinar — Resume Template inside",
        "body": (
            "Hi Alex,\n\nThank you for registering for our 'Land Your Dream Job' webinar! "
            "As promised, here's your free resume template.\n\n"
            "Also check out our 1:1 coaching packages starting at ₹4,999/month.\n\n"
            "Download template → [LINK]\n\nJobCoach India"
        ),
        "sender": "JobCoach India",
        "sender_email": "hello@jobcoach.in",
        "sender_domain": "jobcoach.in",
        "received_at": "2026-04-07T20:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "promotional",
            "priority": "low",
            "action_required": "unsubscribe",
            "deadline_detected": None,
        },
    },
    {
        "email_id": "med_012",
        "subject": "Offer Letter: Senior Engineer — PayU India [Action Required]",
        "body": (
            "Dear Alex,\n\nWe are delighted to extend you an offer for the position of "
            "Senior Software Engineer at PayU India.\n\n"
            "CTC: ₹36 LPA + benefits\nJoining Date: May 5, 2026\n\n"
            "Please review the attached offer letter and revert with your acceptance "
            "by April 11, 2026.\n\nWarm regards,\nDeepika Rao\nHR Business Partner, PayU"
        ),
        "sender": "Deepika Rao",
        "sender_email": "deepika.rao@payu.in",
        "sender_domain": "payu.in",
        "received_at": "2026-04-08T10:45:00Z",
        "has_attachment": True,
        "thread_length": 4,
        "ground_truth": {
            "category": "deadline_alert",
            "priority": "urgent",
            "action_required": "reply",
            "deadline_detected": "2026-04-11",
        },
    },
]

# ─────────────────────────────────────────────
# TASK 3: HARD — Full Pipeline (12 emails)
# Agent must categorize + prioritize + extract deadlines +
# match against candidate profile + draft professional replies
# ─────────────────────────────────────────────
HARD_EMAILS = [
    {
        "email_id": "hard_001",
        "subject": "Senior Python Engineer — Remote FinTech, ₹35-45 LPA — Interested?",
        "body": (
            "Hi Alex,\n\nI'm Neha from TechRecruit Partners. I've been working with "
            "a Series-B FinTech (payments & lending) looking for a Senior Python Engineer.\n\n"
            "Role Details:\n"
            "- Stack: Python, FastAPI, PostgreSQL, AWS, Docker\n"
            "- Experience: 5-8 years\n"
            "- Location: Fully Remote (India)\n"
            "- Comp: ₹35-45 LPA + ESOPs\n\n"
            "This matches your background closely. Would you be open to a 15-min "
            "exploratory call this week? I'm available Thu/Fri afternoons.\n\n"
            "Please respond by Thursday if interested.\n\n"
            "Best,\nNeha Sharma\nTechRecruit Partners"
        ),
        "sender": "Neha Sharma",
        "sender_email": "neha@techrecruitpartners.com",
        "sender_domain": "techrecruitpartners.com",
        "received_at": "2026-04-08T09:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "high",
            "action_required": "reply",
            "deadline_detected": "2026-04-10",
            "profile_match": True,
            "reply_required": True,
            "reply_keywords": ["available", "interested", "call", "thursday", "friday"],
        },
    },
    {
        "email_id": "hard_002",
        "subject": "Java Developer role — 8+ years, Banking domain, On-site Pune",
        "body": (
            "Hi Alex,\n\nHope you're doing well. I came across your profile and wanted "
            "to share an opportunity for a Senior Java Developer at a top private bank.\n\n"
            "Requirements:\n"
            "- Java, Spring Boot, Oracle DB\n"
            "- 8+ years experience\n"
            "- On-site at Pune office (mandatory)\n"
            "- Banking/BFSI domain experience required\n\n"
            "Comp: ₹28-34 LPA\n\n"
            "Let me know if you'd like to explore further.\n\nRegards,\nVikram Joshi"
        ),
        "sender": "Vikram Joshi",
        "sender_email": "vikram@staffingco.in",
        "sender_domain": "staffingco.in",
        "received_at": "2026-04-08T11:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "low",
            "action_required": "archive",
            "deadline_detected": None,
            "profile_match": False,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_003",
        "subject": "URGENT: Offer expires today 6 PM — NexGen Solutions",
        "body": (
            "Dear Alex,\n\nThis is your final reminder. Your offer letter from NexGen Solutions "
            "for the position of Senior Software Engineer (₹38 LPA) expires TODAY at 6:00 PM IST.\n\n"
            "To accept, please sign the offer letter (attached) and email it back, "
            "or call HR directly at +91-9876543210.\n\n"
            "We hope to have you on board!\n\nAnanya Kapoor\nHR Lead, NexGen Solutions"
        ),
        "sender": "Ananya Kapoor",
        "sender_email": "ananya.k@nexgensolutions.com",
        "sender_domain": "nexgensolutions.com",
        "received_at": "2026-04-08T08:00:00Z",
        "has_attachment": True,
        "thread_length": 4,
        "ground_truth": {
            "category": "deadline_alert",
            "priority": "urgent",
            "action_required": "reply",
            "deadline_detected": "2026-04-08",
            "profile_match": True,
            "reply_required": True,
            "reply_keywords": ["accept", "confirm", "sign", "offer"],
        },
    },
    {
        "email_id": "hard_004",
        "subject": "DevOps Engineer (AWS/Kubernetes) — Contract 6 months, Hyderabad",
        "body": (
            "Hi Alex,\n\nWe have an urgent contract opportunity for a DevOps Engineer "
            "with strong AWS and Kubernetes skills.\n\n"
            "Duration: 6-month contract (extendable)\n"
            "Location: Hyderabad (on-site preferred, hybrid possible)\n"
            "Rate: ₹3.5-4 LPA/month\n"
            "Immediate joining required.\n\n"
            "Profile match looks strong. Are you open to contract roles?\n\n"
            "Thanks,\nSunita Rajan\nHorizon Staffing"
        ),
        "sender": "Sunita Rajan",
        "sender_email": "sunita@horizonstaffing.com",
        "sender_domain": "horizonstaffing.com",
        "received_at": "2026-04-08T10:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "low",
            "action_required": "archive",
            "deadline_detected": None,
            "profile_match": False,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_005",
        "subject": "Take-home assignment: Due April 10, 11:59 PM — Meesho Engineering",
        "body": (
            "Hi Alex,\n\nThank you for your interest in the Senior Software Engineer "
            "role at Meesho. As the next step, please complete the attached take-home assignment.\n\n"
            "Time limit: 3 hours (once you begin)\n"
            "Deadline: April 10, 2026 at 11:59 PM IST\n"
            "Submission: Upload at careers.meesho.com/submit\n\n"
            "Please do not share the problem statement with others.\n\n"
            "Best of luck!\nMeesho Engineering Recruiting"
        ),
        "sender": "Meesho Recruiting",
        "sender_email": "engineering-recruiting@meesho.com",
        "sender_domain": "meesho.com",
        "received_at": "2026-04-08T09:30:00Z",
        "has_attachment": True,
        "thread_length": 2,
        "ground_truth": {
            "category": "deadline_alert",
            "priority": "urgent",
            "action_required": "flag",
            "deadline_detected": "2026-04-10",
            "profile_match": True,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_006",
        "subject": "Perfect match: Staff Engineer @ Setu (API infrastructure) — Remote",
        "body": (
            "Hi Alex,\n\nLinkedIn found a job that closely matches your profile:\n\n"
            "Staff Engineer — API Infrastructure at Setu\n"
            "📍 Remote (India) | 💰 ₹42-55 LPA + ESOPs\n"
            "Stack: Python, FastAPI, PostgreSQL, AWS, Kubernetes\n"
            "Domain: FinTech / Financial infrastructure\n"
            "Experience: 5+ years\n\n"
            "This role aligns with your skills and preferred domain.\n"
            "Apply now → [LINK]\n\nLinkedIn Jobs"
        ),
        "sender": "LinkedIn Jobs",
        "sender_email": "jobs-noreply@linkedin.com",
        "sender_domain": "linkedin.com",
        "received_at": "2026-04-08T09:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "job_match",
            "priority": "high",
            "action_required": "apply",
            "deadline_detected": None,
            "profile_match": True,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_007",
        "subject": "Frontend React Developer — 3 years exp, E-commerce, Delhi NCR",
        "body": (
            "Hi Alex,\n\nWe are hiring a Frontend React Developer for our e-commerce client.\n\n"
            "Skills: React, Redux, JavaScript, HTML/CSS\n"
            "Experience: 3 years\n"
            "Location: Delhi NCR (on-site)\n"
            "Salary: ₹10-15 LPA\n\n"
            "Interested? Reply with your CV.\n\nThanks"
        ),
        "sender": "HR Team",
        "sender_email": "hr@quickhire.in",
        "sender_domain": "quickhire.in",
        "received_at": "2026-04-08T08:30:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "low",
            "action_required": "archive",
            "deadline_detected": None,
            "profile_match": False,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_008",
        "subject": "Alex, I'd love to connect — SDE-III at Flipkart Commerce Cloud",
        "body": (
            "Hi Alex,\n\nI'm Arjun, a recruiter at Flipkart Commerce Cloud. "
            "I've been looking at your profile and your work with FastAPI and Docker "
            "is exactly what our platform team needs.\n\n"
            "The SDE-III role offers:\n"
            "- ₹45-58 LPA + RSUs + benefits\n"
            "- Bangalore HQ (hybrid — 2 days/week)\n"
            "- Python/Go backend, Kafka, Redis, PostgreSQL\n\n"
            "I know you prefer remote, so wanted to be upfront about the hybrid model. "
            "Would you still be open to a conversation?\n\n"
            "Let me know by Friday.\n\nArjun Menon\nFlipkart FCC Talent"
        ),
        "sender": "Arjun Menon",
        "sender_email": "arjun.menon@flipkartcommerce.com",
        "sender_domain": "flipkartcommerce.com",
        "received_at": "2026-04-08T11:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "high",
            "action_required": "reply",
            "deadline_detected": "2026-04-11",
            "profile_match": True,
            "reply_required": True,
            "reply_keywords": ["open", "conversation", "hybrid", "bangalore", "flexible"],
        },
    },
    {
        "email_id": "hard_009",
        "subject": "200 new jobs matching Python, AWS, Remote — Weekly Digest",
        "body": (
            "Your weekly job digest — Indeed\n\n"
            "200 jobs matching: Python | AWS | Remote | Bangalore\n\n"
            "Top picks this week:\n"
            "• Senior Python Eng — Razorpay (₹28-38 LPA)\n"
            "• Python Backend — Stripe India (₹40-55 LPA)\n"
            "• DevOps/Python — upGrad (₹20-28 LPA)\n"
            "• ... 197 more\n\nView all → [LINK]\n\nIndeed"
        ),
        "sender": "Indeed Weekly Digest",
        "sender_email": "digest@indeed.com",
        "sender_domain": "indeed.com",
        "received_at": "2026-04-08T06:00:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "job_alert_digest",
            "priority": "normal",
            "action_required": "archive",
            "deadline_detected": None,
            "profile_match": False,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_010",
        "subject": "We're moving forward with other candidates — Paytm",
        "body": (
            "Dear Alex,\n\nThank you for taking the time to interview with Paytm. "
            "After careful deliberation, we have decided to proceed with other candidates "
            "for the Senior Software Engineer position at this time.\n\n"
            "We appreciate your interest in Paytm and encourage you to apply "
            "to future opportunities.\n\nBest wishes,\nPaytm Talent Acquisition"
        ),
        "sender": "Paytm Talent Acquisition",
        "sender_email": "talent@paytm.com",
        "sender_domain": "paytm.com",
        "received_at": "2026-04-07T16:00:00Z",
        "has_attachment": False,
        "thread_length": 5,
        "ground_truth": {
            "category": "application_update",
            "priority": "normal",
            "action_required": "archive",
            "deadline_detected": None,
            "profile_match": False,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_011",
        "subject": "Crack FAANG in 3 months — Free mock interview today",
        "body": (
            "Hi Alex,\n\nWant to work at Google, Amazon or Meta? "
            "Our FAANG prep program has helped 3,000+ engineers land offers.\n\n"
            "🎁 Free mock interview this Saturday — limited spots!\n"
            "Book now → [LINK]\n\nPramp"
        ),
        "sender": "Pramp",
        "sender_email": "hello@pramp.com",
        "sender_domain": "pramp.com",
        "received_at": "2026-04-08T07:45:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "promotional",
            "priority": "low",
            "action_required": "ignore",
            "deadline_detected": None,
            "profile_match": False,
            "reply_required": False,
            "reply_keywords": [],
        },
    },
    {
        "email_id": "hard_012",
        "subject": "Engineering Lead — AI Infra @ Sarvam AI (Remote, ₹50-70 LPA)",
        "body": (
            "Hi Alex,\n\nI'm reaching out from Sarvam AI — India's leading LLM startup "
            "(backed by Lightspeed). We're building AI infrastructure for Indian languages.\n\n"
            "We're hiring an Engineering Lead for our AI Infra team:\n"
            "- Python, FastAPI, AWS, Kubernetes, Docker (your exact stack!)\n"
            "- Remote-first with quarterly offsites in Bangalore\n"
            "- ₹50-70 LPA + meaningful equity\n"
            "- Domain: AI/ML (matches your interests)\n\n"
            "This is an urgent role — we're hoping to close by April 20.\n\n"
            "Would love a 20-minute intro call. Are you free this week?\n\n"
            "Best,\nDivya Krishnan\nHead of Talent, Sarvam AI"
        ),
        "sender": "Divya Krishnan",
        "sender_email": "divya@sarvam.ai",
        "sender_domain": "sarvam.ai",
        "received_at": "2026-04-08T10:15:00Z",
        "has_attachment": False,
        "thread_length": 1,
        "ground_truth": {
            "category": "recruiter_outreach",
            "priority": "high",
            "action_required": "reply",
            "deadline_detected": "2026-04-20",
            "profile_match": True,
            "reply_required": True,
            "reply_keywords": ["available", "interested", "call", "this week", "excited"],
        },
    },
]
