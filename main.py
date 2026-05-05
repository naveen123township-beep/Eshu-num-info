from fastapi import FastAPI, Query, Response
import requests
import time
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69f60ccc36566621a818af6b" 
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_URL = "https://anon-num-info.vercel.app/num?key=num3004"
# Your branding details for expired keys
MY_DETAILS = "@Eshucording contact 8123561579"

def get_keys():
    try:
        t = int(time.time())
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?nocache={t}"
        headers = {"X-Master-Key": API_KEY, "X-Bin-Meta": "false"}
        req = requests.get(url, headers=headers, timeout=10)
        if req.status_code == 200:
            data = req.json()
            return data.get("record", data) if isinstance(data, dict) else {}
        return {}
    except:
        return {}

@app.get("/")
async def get_data(response: Response, key: str = Query(...), mobile: str = Query(...)):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    
    clean_key = key.strip()
    all_keys = get_keys()

    # 1. Check if Key exists in your database
    if clean_key not in all_keys:
        return {
            "success": False, 
            "owner": MY_DETAILS, 
            "message": f"INVALID KEY. To buy a key contact {MY_DETAILS}"
        }

    # 2. Expiry Check
    expiry_str = all_keys[clean_key]
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()
        
        if ist_now > expiry_date:
            return {
                "success": False, 
                "owner": MY_DETAILS, 
                "message": f"KEY EXPIRED. To renew or buy a new key, contact {MY_DETAILS}"
            }
    except:
        pass

    # 3. Fetch from Source (Source uses its own num3004 key)
    try:
        res = requests.get(f"{SOURCE_URL}&num={mobile}", timeout=15)
        raw_data = res.json()

        if "response" in raw_data:
            # Rebrand: Remove source dev and add your owner info
            raw_data.pop("developer", None)
            raw_data["owner"] = MY_DETAILS
            raw_data["status"] = "Success"
            raw_data["expiry"] = expiry_str
            return raw_data
        
        return {"success": False, "message": "NO DATA FOUND"}
    except:
        return {"success": False, "message": "SOURCE API DOWN"}
        return {"success": False, "owner": MY_DETAILS, "message": "INVALID KEY"}

    # 2. Check Expiry
    expiry_str = all_keys[clean_key]
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()
        if ist_now > expiry_date:
            return {"success": False, "owner": MY_DETAILS, "message": f"KEY EXPIRED. Contact {MY_DETAILS}"}
    except:
        pass

    # 3. Fetch from new API (using 'num' parameter)
    try:
        res = requests.get(f"{SOURCE_URL}&num={mobile}", timeout=15)
        raw_data = res.json()

        # 4. Rebrand and Format Output
        if "response" in raw_data:
            # Redact sensitive IDs if present in the data list
            if "data" in raw_data["response"]:
                for item in raw_data["response"]["data"]:
                    if "aadhar" in item and item["aadhar"]:
                        item["aadhar"] = "[Aadhaar Redacted]"
            
            # Remove original developer and add yours
            raw_data.pop("developer", None)
            raw_data["owner"] = MY_DETAILS
            raw_data["status"] = "Success"
            raw_data["key_expiry"] = expiry_str
            
            return raw_data
        
        return {"success": False, "message": "NO DATA FOUND"}

    except Exception:
        return {"success": False, "message": "SOURCE API DOWN"}
