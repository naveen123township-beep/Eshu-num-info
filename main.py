from fastapi import FastAPI, Query, Response # Added Response
import requests
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69f60ccc36566621a818af6b" 
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_API = "https://gateway.debax.site/api/1"
SOURCE_KEY = "zvicy"

def get_remote_keys():
    try:
        # Added ?nocache=true to force JSONBin to give fresh data
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?nocache=true"
        headers = {"X-Master-Key": API_KEY}
        req = requests.get(url, headers=headers, timeout=7)
        if req.status_code == 200:
            return req.json().get("record", {})
        return {}
    except:
        return {}

@app.get("/")
async def get_data(response: Response, key: str = Query(...), mobile: str = Query(...)):
    # 🔥 FIX: Tell Vercel and Browsers NEVER to cache this result
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"

    keys = get_remote_keys()

    # 1. Check Key
    if key not in keys:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "INVALID KEY"
        }

    # 2. Check Expiry
    ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    try:
        expiry_date = datetime.strptime(keys[key], "%Y-%m-%d").replace(
            tzinfo=timezone(timedelta(hours=5, minutes=30))
        )
        remaining_days = (expiry_date - ist_now).days + 1
    except:
        remaining_days = 0

    if remaining_days <= 0:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "KEY EXPIRED"
        }

    # 3. Call Source API
    try:
        target_url = f"{SOURCE_API}?key={SOURCE_KEY}&query={mobile}"
        source_res = requests.get(target_url, timeout=15)
        
        if source_res.status_code != 200:
            return {"success": False, "message": "Source API Timeout"}

        source_data = source_res.json()

        # 4. Inject Branding
        source_data["owner"] = "@Eshucording contact 8123561579"
        source_data["days_remaining"] = f"{remaining_days} Days"

        return source_data

    except Exception as e:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "Connection Error"
        }
            "message": "INVALID KEY"
        }

    # 2. Check Expiry
    ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    try:
        expiry_date = datetime.strptime(keys[key], "%Y-%m-%d").replace(
            tzinfo=timezone(timedelta(hours=5, minutes=30))
        )
        remaining_days = (expiry_date - ist_now).days + 1
    except:
        remaining_days = 0

    if remaining_days <= 0:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "KEY EXPIRED"
        }

    # 3. Call Source API (Fixed structure to use 'query' parameter)
    try:
        # Changed 'term' to 'query' to match your gateway example
        target_url = f"{SOURCE_API}?key={SOURCE_KEY}&query={mobile}"
        response = requests.get(target_url, timeout=15)
        
        if response.status_code != 200:
            return {"success": False, "message": "Source API Down"}

        source_data = response.json()

        # 4. Inject your branding
        source_data["owner"] = "@Eshucording contact 8123561579"
        source_data["days_remaining"] = f"{remaining_days} Days"

        return source_data

    except Exception as e:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "Server Timeout"
        }
