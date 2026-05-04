from fastapi import FastAPI, Query, Response
import requests
import time
from datetime import datetime, timezone, timedelta

app = FastAPI()

BIN_ID = "69f60ccc36566621a818af6b" 
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_URL = "https://ayush-multi-api.vercel.app/api/num"
CONTACT = "@Eshucording contact 8123561579"

def get_keys():
    try:
        # Use a random timestamp to force JSONBin to show the NEW keys
        t = int(time.time())
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?t={t}"
        headers = {"X-Master-Key": API_KEY, "X-Bin-Meta": "false"}
        req = requests.get(url, headers=headers, timeout=10)
        
        if req.status_code == 200:
            res_json = req.json()
            # If JSONBin returns {"record": {...}}, extract the inside
            if isinstance(res_json, dict) and "record" in res_json:
                return res_json["record"]
            return res_json
        return {}
    except:
        return {}

@app.get("/")
async def get_data(response: Response, key: str = Query(...), mobile: str = Query(...)):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    
    user_key = key.strip()
    all_keys = get_keys()

    # --- THE KEY CHECK ---
    if user_key not in all_keys:
        return {"success": False, "owner": CONTACT, "message": "INVALID KEY"}

    # --- EXPIRY CHECK ---
    expiry_str = all_keys[user_key]
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        # Get Current Date in IST
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()

        if ist_now > expiry_date:
            return {
                "success": False, 
                "owner": CONTACT, 
                "message": f"KEY EXPIRED. To buy contact {CONTACT}"
            }
    except:
        pass # If date format is wrong, let them through

    # --- FETCH ORIGINAL DATA ---
    try:
        api_call = requests.get(f"{SOURCE_URL}?term={mobile}", timeout=10)
        data = api_call.json()

        # Remove original dev and add yours
        if isinstance(data, dict):
            data.pop("developer", None)
            data["owner"] = CONTACT
            data["status"] = "Success"
            data["valid_until"] = expiry_str

        return data
    except:
        return {"success": False, "message": "ORIGINAL API ERROR"}
