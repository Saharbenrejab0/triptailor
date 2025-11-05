# TripTailor

Minimal trip planner: you enter destination/dates/interests and it generates a day-by-day itinerary.  
Deterministic algorithm (no external API by default).

## Run
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run web/main.py
