from fastapi import FastAPI, Query
import requests
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69eec211aaba8821973f621a"
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_API = "https://api.subhxcosmo.in/api"
SOURCE_KEY = "CYBERXZEXX"

# --- GET KEYS FROM JSONBIN ---
def get_remote_keys():
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        req = requests.get(url, headers=headers)
        return req.json().get("record", {})
    except:
        return {}

# --- MAIN API ---
@app.get("/")
async def get_data(key: str = Query(...), mobile: str = Query(...)):
    keys = get_remote_keys()

    # ❌ INVALID KEY
    if key not in keys:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "INVALID KEY"
        }

    # ✅ IST TIME
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

    try:
        expiry_date = datetime.strptime(keys[key], "%Y-%m-%d").replace(
            tzinfo=timezone(timedelta(hours=5, minutes=30))
        )
        remaining_days = (expiry_date - ist_now).days + 1
    except:
        remaining_days = 0

    # ❌ EXPIRED KEY
    if remaining_days <= 0:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "KEY EXPIRED TO BUY CALL 8123561579"
        }

    try:
        # 🔗 CALL SOURCE API
        response = requests.get(
            f"{SOURCE_API}?key={SOURCE_KEY}&type=mobile&term={mobile}",
            timeout=10
        )

        source_data = response.json()

        # 🔥 ONLY MODIFY OWNER
        source_data["owner"] = "@Eshucording contact 8123561579"

        # 🔥 ADD DAYS WITHOUT BREAKING STRUCTURE
        source_data["days_remaining"] = f"{remaining_days} Days"

        return source_data

    except Exception as e:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "Source API Connection Error"
        }