from datetime import date, timedelta
from typing import Dict, List

def daterange(start_iso: str, end_iso: str) -> List[str]:
    s = date.fromisoformat(start_iso); e = date.fromisoformat(end_iso)
    out = []
    cur = s
    while cur <= e:
        out.append(cur.isoformat())
        cur += timedelta(days=1)
    return out

def suggest_time_slots(pace: str) -> List[str]:
    if pace == "relaxed":
        return ["10:00-12:00", "13:00-15:00"]
    if pace == "intense":
        return ["08:30-11:30", "12:00-14:00", "14:30-17:30", "19:00-21:00"]
    return ["09:00-11:30", "12:00-14:00", "15:00-17:30"]

def rough_cost(budget_level: str) -> float:
    return {"low": 35.0, "mid": 80.0, "high": 180.0}.get(budget_level, 80.0)

def neighborhood_hints(destination: str, interests: List[str]) -> Dict[str, List[str]]:
    base = {
        "museums": ["Historic Center", "Museum Quarter"],
        "food": ["Old Town", "Riverside Market"],
        "nature": ["City Park", "Botanical Gardens"],
        "shopping": ["Main Avenue", "Artsy District"],
        "nightlife": ["Waterfront", "Artsy District"],
        "architecture": ["Old Quarter", "Landmarks Axis"],
        "beach": ["Seafront", "Harbor"],
    }
    picks = []
    for k in (interests or ["museums", "food"]):
        picks += base.get(k, [])
    seen, areas = set(), []
    for p in picks:
        if p not in seen:
            seen.add(p); areas.append(p)
    return {"areas": areas[:4] or ["Central"]}
