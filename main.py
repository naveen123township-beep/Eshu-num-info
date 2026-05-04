from fastapi import FastAPI, Query, Response
import requests
import time
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69f60ccc36566621a818af6b" 
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_URL = "https://ayush-multi-api.vercel.app/api/num"
CONTACT_INFO = "@Eshucording contact 8123561579"

def get_remote_keys():
    try:
        t = int(time.time())
        # Forces fresh data so new keys work immediately
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?nocache=true&t={t}"
        headers = {"X-Master-Key": API_KEY, "X-Bin-Meta": "false"}
        req = requests.get(url, headers=headers, timeout=10)
        
        if req.status_code == 200:
            data = req.json()
            # Bot saves data inside "record", so we must read from "record"
            return data.get("record", data) 
        return {}
    except:
        return {}

@app.get("/")
async def get_data(response: Response, key: str = Query(...), mobile: str = Query(...)):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    
    clean_key = key.strip()
    keys_data = get_remote_keys()

    # 1. Key Validation
    if not keys_data or clean_key not in keys_data:
        return {
            "success": False, 
            "owner": CONTACT_INFO, 
            "message": "INVALID KEY"
        }

    # 2. Expiry Logic (IST / UTC comparison)
    expiry_date_str = keys_data[clean_key]
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").date()
        # Current date in IST (UTC+5:30)
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()

        if ist_now > expiry_date:
            return {
                "success": False,
                "owner": CONTACT_INFO,
                "message": f"KEY EXPIRED. To buy contact {CONTACT_INFO}"
            }
    except Exception as e:
        # If date format is weird, we let it pass but log the error
        pass

    # 3. Fetch Data from Original Source
    try:
        source_res = requests.get(f"{SOURCE_URL}?term={mobile}", timeout=10)
        if source_res.status_code != 200:
            return {"success": False, "message": "SOURCE API DOWN"}
        
        data = source_res.json()

        # 4. Remove Ayush and inject Eshu Branding
        if isinstance(data, dict):
            data.pop("developer", None) # Remove original dev
            data["owner"] = CONTACT_INFO
            data["status"] = "Success"
            data["key_valid_until"] = expiry_date_str

        return data

    except Exception:
        return {"success": False, "message": "INTERNAL SERVER ERROR"}

    # 1. Key Check (Now checking inside the record)
    if not keys_data or clean_key not in keys_data:
        return {
            "success": False, 
            "owner": "@Eshucording contact 8123561579", 
            "message": "INVALID KEY"
        }

    # 2. Expiry Logic
    expiry_date_str = keys_data[clean_key]
    try:
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)

        if current_time > expiry_date:
            return {
                "success": False,
                "message": "KEY EXPIRED. To buy contact @Eshucording or 8123561579"
            }
    except:
        pass

    # 3. Fetch Data from Source
    try:
        source_res = requests.get(f"{SOURCE_URL}?term={mobile}", timeout=10)
        if source_res.status_code != 200:
            return {"success": False, "message": "SOURCE API ERROR"}
        
        data = source_res.json()

        # 4. Rebrand Output
        if isinstance(data, dict):
            data.pop("developer", None) # Remove Ayush branding
            data["owner"] = "@Eshucording contact 8123561579"
            data["status"] = "Success"
            data["expiry"] = expiry_date_str

        return data

    except Exception:
        return {"success": False, "message": "SERVER ERROR"}
