from typing import List
from .schemas import TripRequest, TripPlan, DayPlan, Activity
from .enrichers import daterange, suggest_time_slots, rough_cost, neighborhood_hints

def _activity_templates(interests: List[str]) -> List[str]:
    if not interests:
        interests = ["museums", "food"]
    bank = {
        "museums": ["Top Museum", "Hidden Gallery"],
        "food": ["Local Food Tour", "Street Food Walk"],
        "nature": ["Panoramic Park Walk", "Lakeside Stroll"],
        "shopping": ["Crafts Market", "Design Shops"],
        "nightlife": ["Rooftop Bar", "Live Music Spot"],
        "architecture": ["Iconic Landmark", "Old Quarter Stroll"],
        "beach": ["Beach Time", "Sunset Walk"]
    }
    titles: List[str] = []
    for k in interests:
        titles += bank.get(k, [])
    return (titles or ["City Highlights"])[:8]

def plan_trip(req: TripRequest) -> TripPlan:
    dates = daterange(req.start_date, req.end_date)
    slots = suggest_time_slots(req.pace)
    per_act_cost = rough_cost(req.budget_level) / max(len(slots), 1)
    areas = neighborhood_hints(req.destination, req.interests)["areas"]
    templates = _activity_templates(req.interests)

    days: List[DayPlan] = []
    total_cost = 0.0

    for i, d in enumerate(dates):
        acts: List[Activity] = []
        for j, slot in enumerate(slots):
            title = templates[(i + j) % len(templates)]
            area = areas[(i + j) % len(areas)]
            acts.append(Activity(
                title=title,
                time=slot,
                area=area,
                est_cost=round(per_act_cost, 2),
                notes="Book ahead if required."
            ))
            total_cost += per_act_cost

        days.append(DayPlan(
            date=d,
            summary=f"{req.destination}: {req.pace.capitalize()} day focused on {', '.join(req.interests) or 'highlights'}.",
            activities=acts
        ))

    return TripPlan(destination=req.destination, days=days, total_est_cost=round(total_cost, 2))
