from fastapi import FastAPI, Query
import requests
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69eec211aaba8821973f621a"
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"

SOURCE_API = "https://gateway.debax.site/api/1"
SOURCE_AUTH_KEY = "zvicy" 
OWNER_TAG = "@Eshucording contact 8123561579"

def get_remote_keys():
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        req = requests.get(url, headers=headers, timeout=5)
        return req.json().get("record", {})
    except Exception:
        return {}

# Changed endpoint to "/" to match your desired link structure
@app.get("/")
async def get_data(key: str = Query(...), mobile: str = Query(...)):
    keys = get_remote_keys()

    if key not in keys:
        return {"success": False, "owner": OWNER_TAG, "message": "INVALID KEY"}

    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    try:
        expiry_date = datetime.strptime(keys[key], "%Y-%m-%d").replace(
            tzinfo=timezone(timedelta(hours=5, minutes=30))
        )
        remaining_days = (expiry_date - ist_now).days + 1
    except Exception:
        remaining_days = 0

    if remaining_days <= 0:
        return {"success": False, "owner": OWNER_TAG, "message": "KEY EXPIRED"}

    try:
        # Internally converts your 'mobile' param to 'query' for the source
        response = requests.get(
            f"{SOURCE_API}?key={SOURCE_AUTH_KEY}&query={mobile}", 
            timeout=10
        )
        source_data = response.json()

        return {
            "owner": OWNER_TAG,
            "days_remaining": f"{remaining_days} Days",
            "count": source_data.get("count", 0),
            "results": source_data.get("results", [])
        }
    except Exception:
        return {"success": False, "owner": OWNER_TAG, "message": "Source API Error"}
