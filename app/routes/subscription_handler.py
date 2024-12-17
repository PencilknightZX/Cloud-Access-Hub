from fastapi import APIRouter, HTTPException
from database import subscriptions_collection
from typing import Dict

router = APIRouter()

@router.post("/")
async def subscribe_user(subscription: Dict):
    if "user_id" not in subscription or "plan_name" not in subscription:
        raise HTTPException(status_code=400, detail="Missing required fields: user_id or plan_name")
    result = await subscriptions_collection.collection.insert_one(subscription)
    return {
                "message": "User subscribed successfully", 
                "subscription_id": str(result.inserted_id)
            }

@router.get("/{user_id}")
async def get_user_subscription(user_id: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    subscription["_id"] = str(subscription["_id"])
    return subscription
