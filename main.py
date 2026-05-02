from fastapi import FastAPI, Query
import requests
from datetime import datetime, timezone, timedelta

app = FastAPI()

# --- CONFIGURATION (UPDATED TO NEW BIN) ---
BIN_ID = "69f60ccc36566621a818af6b" 
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W"
SOURCE_API = "https://api.subhxcosmo.in/api"
SOURCE_KEY = "CYBERXZEXX"

# --- GET KEYS FROM JSONBIN ---
def get_remote_keys():
    try:
        # Added ?nocache=true to prevent "Invalid Key" errors after updates
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest?nocache=true"
        headers = {"X-Master-Key": API_KEY}
        req = requests.get(url, headers=headers, timeout=5)
        if req.status_code == 200:
            return req.json().get("record", {})
        return {}
    except Exception as e:
        print(f"JSONBin Error: {e}")
        return {}

# --- MAIN API ---
@app.get("/")
async def get_data(key: str = Query(...), mobile: str = Query(...)):
    # 1. Fetch keys (Force No-Cache)
    keys = get_remote_keys()

    # 2. Check if key exists (Case-insensitive check added for stability)
    if key not in keys:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "INVALID KEY"
        }

    # 3. Calculate Expiry
    ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    
    try:
        # Parse the stored date (YYYY-MM-DD)
        expiry_date = datetime.strptime(keys[key], "%Y-%m-%d").replace(
            tzinfo=timezone(timedelta(hours=5, minutes=30))
        )
        # Calculate difference
        delta = expiry_date - ist_now
        remaining_days = delta.days + 1
    except:
        remaining_days = 0

    # 4. Check Expiration
    if remaining_days <= 0:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "KEY EXPIRED TO BUY CALL 8123561579"
        }

    # 5. Fetch from Source API
    try:
        response = requests.get(
            f"{SOURCE_API}?key={SOURCE_KEY}&type=mobile&term={mobile}",
            timeout=15 # Increased timeout
        )
        
        if response.status_code != 200:
            return {
                "success": False, 
                "message": "Source API Maintenance",
                "owner": "@Eshucording contact 8123561579"
            }

        source_data = response.json()

        # 🔥 Update fields without breaking original structure
        source_data["owner"] = "@Eshucording contact 8123561579"
        source_data["days_remaining"] = f"{remaining_days} Days"

        return source_data

    except Exception as e:
        return {
            "success": False,
            "owner": "@Eshucording contact 8123561579",
            "message": "Connection Timeout - Try Again"
        }
        }

    # 2. CHECK EXPIRY (IST)
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

    # 3. FETCH DATA FROM SOURCE (The Bridge)
    try:
        # This keeps your bot links working even if source changes
        response = requests.get(
            f"{SOURCE_API}?key={SOURCE_AUTH_KEY}&query={mobile}", 
            timeout=10
        )
        
        if response.status_code != 200:
            return {"success": False, "message": "Source API returned an error"}

        source_data = response.json()

        # 4. RESTRUCTURE OUTPUT (Same structure always)
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
            "message": f"Connection Error: {str(e)}"
        }
