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
        t = int(time.time())
        # Forces the most recent update from your bot
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?nocache={t}"
        headers = {"X-Master-Key": API_KEY, "X-Bin-Meta": "false"}
        req = requests.get(url, headers=headers, timeout=10)
        
        if req.status_code == 200:
            data = req.json()
            # Smart check: if 'record' exists, use it. If not, use data.
            if isinstance(data, dict):
                return data.get("record", data)
            return data
        return {}
    except:
        return {}

@app.get("/")
async def get_data(response: Response, key: str = Query(...), mobile: str = Query(...)):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    
    user_key = key.strip()
    keys_data = get_keys()

    # 1. Check if key exists
    if user_key not in keys_data:
        return {"success": False, "owner": CONTACT, "message": "INVALID KEY"}

    # 2. Expiry Check
    expiry_str = keys_data[user_key]
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()

        if ist_now > expiry_date:
            return {"success": False, "owner": CONTACT, "message": f"KEY EXPIRED. Buy: {CONTACT}"}
    except:
        pass

    # 3. Fetch from Ayush API and Rebrand
    try:
        res = requests.get(f"{SOURCE_URL}?term={mobile}", timeout=10)
        data = res.json()
        if isinstance(data, dict):
            data.pop("developer", None)
            data["owner"] = CONTACT
            data["status"] = "Success"
            data["expiry"] = expiry_str
        return data
    except:
        return {"success": False, "message": "API SERVER BUSY"}
    # 1. Validation
    if input_key not in db_keys:
        return {"success": False, "owner": CONTACT, "message": "INVALID KEY"}

    # 2. Expiry Check (IST Time)
    expiry_str = db_keys[input_key]
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()

        if ist_now > expiry_date:
            return {
                "success": False, 
                "owner": CONTACT, 
                "message": f"KEY EXPIRED. To buy contact {CONTACT}"
            }
    except:
        pass # If date format error, allow access

    # 3. Data Fetching
    try:
        res = requests.get(f"{SOURCE_URL}?term={mobile}", timeout=10)
        final_data = res.json()
        
        if isinstance(final_data, dict):
            final_data.pop("developer", None) # Remove Ayush
            final_data["owner"] = CONTACT # Add Eshu
            final_data["status"] = "Success"
            final_data["key_expiry"] = expiry_str
            
        return final_data
    except:
        return {"success": False, "message": "ORIGINAL API ERROR"}

    # --- 1. CRITICAL KEY CHECK ---
    if user_key not in all_keys:
        return {"success": False, "owner": CONTACT, "message": "INVALID KEY"}

    # --- 2. EXPIRY CHECK ---
    expiry_str = all_keys[user_key]
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()

        if ist_now > expiry_date:
            return {
                "success": False, 
                "owner": CONTACT, 
                "message": f"KEY EXPIRED. To buy contact {CONTACT}"
            }
    except:
        pass

    # --- 3. FETCH AND CLEAN DATA ---
    try:
        source_call = requests.get(f"{SOURCE_URL}?term={mobile}", timeout=10)
        source_data = source_call.json()

        if isinstance(source_data, dict):
            # Remove developer and rebrand
            source_data.pop("developer", None)
            source_data["owner"] = CONTACT
            source_data["status"] = "Success"
            source_data["valid_until"] = expiry_str
            
        return source_data
    except:
        return {"success": False, "message": "ORIGINAL API ERROR"}

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
