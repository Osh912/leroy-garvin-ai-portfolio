from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field


class JobOut(BaseModel):
    id: int
    external_id: str
    source: str
    source_display: str = ""
    company: str
    title: str
    location: str
    is_remote: bool
    remote_verified: bool = False
    remote_verified_label: str = "✗ Not Verified Remote"
    salary_text: str
    salary_min: float | None = None
    salary_max: float | None = None
    url: str
    posting_url: str = ""
    careers_url: str = ""
    description: str
    tags: str
    level_hint: str
    score: float
    match_score: float = 0
    match_percentage: float = 0
    interview_probability: float | None = None
    estimated_salary: str = ""
    why_match: str = ""
    score_breakdown: dict[str, Any] = Field(default_factory=dict)
    matched_projects: list[dict[str, Any]] = Field(default_factory=list)
    found_at: datetime
    date_found: str = ""
    last_verified_at: str | None = None
    is_active: bool = True
    package_ready: bool = False
    posted_at: datetime | None = None
    status: str
    rank: int | None = None
    is_top_10: bool = False

    class Config:
        from_attributes = True


class ManualJobIn(BaseModel):
    company: str
    title: str
    location: str = "Remote, United States"
    url: str = ""
    salary_text: str = ""
    description: str
    source: str = "manual"


class ApplicationIn(BaseModel):
    job_id: int | None = None
    company: str
    position: str
    salary: str = ""
    location: str = "Remote"
    date_applied: date | None = None
    status: str = "saved"
    follow_up_date: date | None = None
    interview_date: date | None = None
    notes: str = ""
    recruiter_name: str = ""
    recruiter_email: str = ""
    tailored_resume: str = ""
    cover_letter: str = ""
    interview_prep: dict[str, Any] = Field(default_factory=dict)
    portfolio_refs: list[dict[str, Any]] = Field(default_factory=list)
    application_score: float = 0


class ApplicationUpdate(BaseModel):
    company: str | None = None
    position: str | None = None
    salary: str | None = None
    location: str | None = None
    date_applied: date | None = None
    status: str | None = None
    follow_up_date: date | None = None
    interview_date: date | None = None
    notes: str | None = None
    recruiter_name: str | None = None
    recruiter_email: str | None = None
    tailored_resume: str | None = None
    cover_letter: str | None = None
    interview_prep: dict[str, Any] | None = None
    analytics: dict[str, Any] | None = None
    portfolio_refs: list[dict[str, Any]] | None = None
    application_score: float | None = None


class ApplicationOut(BaseModel):
    id: int
    job_id: int
    company: str
    position: str
    salary: str
    location: str
    date_applied: date | None
    status: str
    stage_label: str = ""
    follow_up_date: date | None
    interview_date: date | None
    notes: str
    recruiter_name: str
    recruiter_email: str
    tailored_resume: str
    cover_letter: str
    interview_prep: dict[str, Any] = Field(default_factory=dict)
    analytics: dict[str, Any] = Field(default_factory=dict)
    portfolio_refs: list[dict[str, Any]]
    application_score: float
    interview_probability: float = 0
    portfolio_url: str = "https://leroy-garvin-ai-portfolio.vercel.app"
    approval_required: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class GenerateOut(BaseModel):
    job_id: int
    score: float
    score_breakdown: dict[str, Any]
    matched_projects: list[dict[str, Any]]
    tailored_resume: str
    cover_letter: str
    why_match: str = ""
    interview_probability: float = 0
    used_ai: bool
    truth_warnings: list[str] = Field(default_factory=list)
    auto_apply: bool = False
    approval_required: bool = True


class InterviewPrepOut(BaseModel):
    job_id: int
    application_id: int | None = None
    company: str
    title: str
    prep: dict[str, Any]
    prep_markdown: str
    packet_paths: dict[str, str] = Field(default_factory=dict)
    auto_apply: bool = False


class ExportOut(BaseModel):
    job_id: int | None = None
    application_id: int | None = None
    resume_filename: str
    cover_filename: str
    resume: str
    cover_letter: str
    portfolio_url: str
    export_note: str


class HighestInterviewOut(BaseModel):
    application_id: int
    job_id: int
    company: str
    position: str
    status: str
    interview_date: str | None = None
    interview_probability: float


class DashboardOut(BaseModel):
    new_jobs_today: int
    applications_ready: int = 0
    applications_sent: int
    interviews_scheduled: int = 0
    interviews: int
    follow_ups_due: int
    highest_probability_interview_this_week: HighestInterviewOut | None = None
    best_new_opportunities: list[JobOut]
    recent_applications: list[ApplicationOut]
    status_counts: dict[str, int]
    auto_apply: bool = False
    mode: str = "production"
    last_refresh: dict[str, Any] | None = None
    refreshed_at: str | None = None
