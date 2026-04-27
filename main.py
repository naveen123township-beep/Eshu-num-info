from fastapi import FastAPI, Query
import requests
from datetime import datetime, timezone, timedelta
from collections import OrderedDict

app = FastAPI()

# --- CONFIGURATION ---
BIN_ID = "69eec211aaba8821973f621a"
API_KEY = "$2a$10$e7Ap4ivHIhQer/PSEZXQmO.PO.oafbEncIR6ZIgQmGqCTBUm3b25W" 
SOURCE_API = "https://hitackgrop-19xe.vercel.app/get_data"

def get_remote_keys():
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        req = requests.get(url, headers=headers)
        return req.json().get("record", {})
    except:
        return {}

@app.get("/")
async def get_data(key: str = Query(...), mobile: str = Query(...)):
    keys = get_remote_keys()
    
    if key not in keys:
        return {"status": "error", "message": "INVALID KEY", "DEVLOPER": "@Eshucording"}
    
    # IST Expiry Logic
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    try:
        expiry_date = datetime.strptime(keys[key], "%Y-%m-%d").replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
        remaining_days = (expiry_date - ist_now).days + 1
    except:
        remaining_days = 0
    
    if remaining_days <= 0:
        return {"status": "error", "message": "KEY EXPIRED TO BUY CALL 8123561579", "DEVLOPER": "@Eshucording"}

    try:
        response = requests.get(f"{SOURCE_API}?key=ottt&mobile={mobile}", timeout=10)
        source_data = response.json()
        
        # Exact order: Days Remaining first, Developer last
        output = OrderedDict()
        output["days_remaining"] = f"{remaining_days} Days"
        output["total_records"] = source_data.get("total_records", 0)
        output["data"] = source_data.get("data", [])
        output["DEVLOPER"] = "@Eshucording"
        return output
    except:
        return {"error": "Source API Connection Error", "DEVLOPER": "@Eshucording"}
