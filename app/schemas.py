from pydantic import BaseModel, Field
from typing import List, Optional

class TripRequest(BaseModel):
    destination: str
    start_date: str  # ISO: YYYY-MM-DD
    end_date: str
    interests: List[str] = Field(default_factory=list)
    budget_level: str = "mid"   # "low" | "mid" | "high"
    pace: str = "balanced"      # "relaxed" | "balanced" | "intense"

class Activity(BaseModel):
    title: str
    time: str      # ex: "09:00-11:30"
    area: str
    notes: Optional[str] = None
    est_cost: Optional[float] = None

class DayPlan(BaseModel):
    date: str
    summary: str
    activities: List[Activity] = Field(default_factory=list)

class TripPlan(BaseModel):
    destination: str
    days: List[DayPlan]
    total_est_cost: Optional[float] = None
