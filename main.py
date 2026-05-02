from fastapi import FastAPI, Query, Response
import requests
import time
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69f60ccc36566621a818af6b" 
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_API = "https://gateway.debax.site/api/1"
SOURCE_KEY = "zvicy"

def get_remote_keys():
    try:
        # Use a unique timestamp to force JSONBin to give fresh data every second
        timestamp = int(time.time())
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?nocache=true&t={timestamp}"
        headers = {
            "X-Master-Key": API_KEY,
            "X-Bin-Meta": "false" # Tells JSONBin to only send the data, not metadata
        }
        req = requests.get(url, headers=headers, timeout=10)
        if req.status_code == 200:
            return req.json() # Returns the dict of keys
        return {}
    except:
        return {}

@app.get("/")
async def get_data(response: Response, key: str = Query(...), mobile: str = Query(...)):
    # 🚫 STOP VERCEL CACHING
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # 1. Clean the input key (Removes extra spaces)
    clean_key = key.strip()

    # 2. Get fresh keys from JSONBin
    keys = get_remote_keys()

    # 3. Check Key (Case-Sensitive check)
    if clean_key not in keys:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": f"INVALID KEY: {clean_key}"
        }

    # 4. Check Expiry
    ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    try:
        expiry_date = datetime.strptime(keys[clean_key], "%Y-%m-%d").replace(
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

    # 5. Call Source API
    try:
        target_url = f"{SOURCE_API}?key={SOURCE_KEY}&query={mobile}"
        source_res = requests.get(target_url, timeout=15)
        
        if source_res.status_code != 200:
            return {"success": False, "message": "Gateway Offline"}

        source_data = source_res.json()
        source_data["owner"] = "@Eshucording contact 8123561579"
        source_data["days_remaining"] = f"{remaining_days} Days"

        return source_data

    except Exception as e:
        return {"success": False, "message": "Connection Timeout"}
