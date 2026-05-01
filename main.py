from fastapi import FastAPI, Query
import requests
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69eec211aaba8821973f621a"
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"

# New Source API Configuration
SOURCE_API = "https://gateway.debax.site/api/1"
OWNER_TAG = "@Eshucording contact 8123561579"

# --- GET KEYS FROM JSONBIN ---
def get_remote_keys():
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        req = requests.get(url, headers=headers, timeout=5)
        return req.json().get("record", {})
    except Exception:
        return {}

# --- UPDATED API ENDPOINT ---
@app.get("/api/1")
async def get_data(key: str = Query(...), query: str = Query(...)):
    keys = get_remote_keys()

    # 1. VALIDATE KEY
    if key not in keys:
        return {
            "success": False,
            "owner": OWNER_TAG,
            "message": "INVALID KEY"
        }

    # 2. CALCULATE EXPIRY (IST)
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    try:
        expiry_date = datetime.strptime(keys[key], "%Y-%m-%d").replace(
            tzinfo=timezone(timedelta(hours=5, minutes=30))
        )
        remaining_days = (expiry_date - ist_now).days + 1
    except Exception:
        remaining_days = 0

    if remaining_days <= 0:
        return {
            "success": False,
            "owner": OWNER_TAG,
            "message": "KEY EXPIRED TO BUY CALL 8123561579"
        }

    # 3. FETCH DATA FROM NEW SOURCE
    try:
        # Note: We pass the query parameter as required by the new source
        response = requests.get(
            f"{SOURCE_API}?key={key}&query={query}", 
            timeout=10
        )
        source_data = response.json()

        # 4. RESTRUCTURE DATA
        # Remove old 'DEV' tag if it exists and inject your 'owner' tag
        if "DEV" in source_data:
            del source_data["DEV"]
            
        final_response = {
            "owner": OWNER_TAG,
            "days_remaining": f"{remaining_days} Days",
            "count": source_data.get("count", 0),
            "results": source_data.get("results", [])
        }

        return final_response

    except Exception as e:
        return {
            "success": False,
            "owner": OWNER_TAG,
            "message": "Source API Connection Error"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
