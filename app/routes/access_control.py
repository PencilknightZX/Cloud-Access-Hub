from fastapi import APIRouter, HTTPException
from database import subscriptions_collection
from typing import Dict

router = APIRouter()

@router.post("/check_access/")
async def check_access(request: Dict):
    user_id = request.get("user_id")
    api_endpoint = request.get("api_endpoint")

    if not user_id or not api_endpoint:
        raise HTTPException(status_code=400, detail="Missing user_id or api_endpoint")
    
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription or api_endpoint not in subscription.get("permissions", []):
        raise HTTPException(status_code=403, detail="Access denied")

    return {"message": "Access granted"}
