from app.schemas import TripRequest
from app.planner import plan_trip

def test_basic_plan():
    req = TripRequest(
        destination="Lisbon",
        start_date="2025-11-10",
        end_date="2025-11-12",
        interests=["food","museums"],
        budget_level="mid",
        pace="balanced"
    )
    plan = plan_trip(req)
    assert plan.destination == "Lisbon"
    assert len(plan.days) == 3
    assert plan.total_est_cost and plan.total_est_cost > 0
