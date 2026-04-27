from fastapi import FastAPI, HTTPException, Query
import requests
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os

app = FastAPI()

# --- CONFIGURATION ---
# Replace with your actual MongoDB URL from MongoDB Atlas
MONGO_URL = "your_mongodb_connection_string"
client = AsyncIOMotorClient(MONGO_URL)
db = client["api_database"]
keys_col = db["keys"]

ORIGINAL_API = "https://hitackgrop-19xe.vercel.app/get_data"

@app.get("/")
async def get_data(key: str = Query(...), mobile: str = Query(...)):
    # 1. Check Database for Key
    key_data = await keys_col.find_one({"key": key})
    
    if not key_data:
        raise HTTPException(status_code=403, detail="INVALID KEY")
    
    # 2. Expiry Calculation
    expiry_date = datetime.strptime(key_data["expiry"], "%Y-%m-%d")
    remaining_days = (expiry_date - datetime.now()).days
    
    if remaining_days < 0:
        return {"status": "error", "message": "KEY EXPIRED TO BUY CALL 8123561579"}

    # 3. Fetch Data
    try:
        response = requests.get(f"{ORIGINAL_API}?key=ottt&mobile={mobile}")
        data = response.json()
        
        # 4. Final Formatted Output
        return {
            "days_remaining": f"{remaining_days} Days",
            "total_records": data.get("total_records", 0),
            "data": data.get("data", []),
            "DEVELOPER": "@Eshucording"
        }
    except:
        return {"status": "error", "message": "Source API Error"}
        