from fastapi import FastAPI, Query, Response
import requests
import time

app = FastAPI()

# --- CONFIG ---
BIN_ID = "69f60ccc36566621a818af6b" 
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_URL = "https://anon-num-info.vercel.app/num?key=num3004"
MY_DETAILS = "@Eshucording contact 8123561579"

@app.get("/")
async def get_data(response: Response, key: str = Query(...), mobile: str = Query(...)):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    
    # 1. Fetch fresh data from JSONBin
    try:
        t = int(time.time())
        db_url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?nocache={t}"
        headers = {"X-Master-Key": API_KEY, "X-Bin-Meta": "false"}
        db_res = requests.get(db_url, headers=headers, timeout=10)
        all_keys = db_res.json()
        
        # If JSONBin returns a list or a nested 'record'
        if isinstance(all_keys, dict) and "record" in all_keys:
            all_keys = all_keys["record"]
            
    except Exception as e:
        return {"success": False, "message": "Database Error", "error": str(e)}

    # 2. Direct Key Check
    if key not in all_keys:
        return {
            "success": False, 
            "owner": MY_DETAILS, 
            "message": f"INVALID KEY. Contact {MY_DETAILS}",
            "debug_received_key": key
        }

    # 3. Fetch from Original API
    try:
        # Use mobile parameter for the source
        source_res = requests.get(f"{SOURCE_URL}&num={mobile}", timeout=15)
        data = source_res.json()

        if "response" in data:
            # Swap developer for your branding
            data.pop("developer", None)
            data["owner"] = MY_DETAILS
            data["status"] = "Success"
            data["key_used"] = key
            return data
        
        return {"success": False, "message": "Number not found in source database."}

    except:
        return {"success": False, "message": "Source API Connection Failed"}
            "owner": MY_DETAILS, 
            "message": f"INVALID KEY. Contact {MY_DETAILS} to buy."
        }

    # 2. Key is valid, now fetch from the original source API
    try:
        # Forward the request using the source's required internal key
        source_res = requests.get(f"{SOURCE_URL}&num={mobile}", timeout=15)
        data = source_res.json()

        # 3. Rebrand: Remove their developer link and add yours
        if "response" in data:
            data.pop("developer", None) # Remove original dev
            data["owner"] = MY_DETAILS    # Add your branding
            data["status"] = "Success"
            return data
        
        return {"success": False, "message": "No data found for this number."}

    except Exception:
        return {"success": False, "message": "Original API is currently down."}

    # 1. KEY VALIDATION
    if clean_key not in all_keys:
        return {"success": False, "owner": MY_DETAILS, "message": "INVALID KEY"}

    # 2. EXPIRY CHECK
    expiry_str = all_keys[clean_key]
    try:
        expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d").date()
        ist_now = (datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)).date()
        if ist_now > expiry_date:
            return {"success": False, "owner": MY_DETAILS, "message": f"KEY EXPIRED. Contact {MY_DETAILS}"}
    except:
        pass

    # 3. CONNECT TO ORIGINAL API
    try:
        # Sending request to the original source with the correct 'num' parameter
        res = requests.get(f"{SOURCE_URL}&num={mobile}", timeout=15)
        raw_data = res.json()

        # 4. SWAP DEVELOPER DETAILS
        if "response" in raw_data:
            # We remove the original developer and insert your branding
            raw_data.pop("developer", None)
            raw_data["owner"] = MY_DETAILS
            raw_data["status"] = "Success"
            raw_data["key_expiry"] = expiry_str
            
            return raw_data
        
        return {"success": False, "message": "NO DATA FOUND FROM SOURCE"}

    except Exception:
        return {"success": False, "message": "ORIGINAL API CONNECTION ERROR"}
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
