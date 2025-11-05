# --- make parent folder importable (DOIT être tout en haut) ---
import os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# --------------------------------------------------------------

import streamlit as st
from app.schemas import TripRequest
from app.planner import plan_trip

st.set_page_config(page_title="TripTailor", page_icon="🧭", layout="wide")
st.title("🧭 TripTailor — Your Own Trip Planner")

with st.form("plan-form"):
    cols = st.columns(2)
    destination = cols[0].text_input("Destination", value="Barcelona")
    interests = cols[1].multiselect(
        "Interests",
        ["museums","food","nature","shopping","nightlife","architecture","beach"],
        default=["museums","food"]
    )
    start_date = cols[0].date_input("Start date")
    end_date   = cols[1].date_input("End date")
    budget = cols[0].selectbox("Budget level", ["low","mid","high"], index=1)
    pace = cols[1].selectbox("Daily pace", ["relaxed","balanced","intense"], index=1)
    submitted = st.form_submit_button("Generate Itinerary")

if submitted:
    req = TripRequest(
        destination=destination.strip(),
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        interests=interests,
        budget_level=budget,
        pace=pace
    )
    plan = plan_trip(req)
    st.subheader(f"Itinerary: {plan.destination} ({len(plan.days)} days)")
    st.caption(f"Estimated total cost: ~€{plan.total_est_cost:.0f}")
    for d in plan.days:
        with st.expander(f"📅 {d.date} — {d.summary}"):
            for a in d.activities:
                st.markdown(f"- **{a.time}** — **{a.title}** in _{a.area}_  · est. €{a.est_cost}")

    st.download_button(
        "Download JSON",
        data=plan.model_dump_json(indent=2),
        file_name=f"{plan.destination}_plan.json",
        mime="application/json"
    )
