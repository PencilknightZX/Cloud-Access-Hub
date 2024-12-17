from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.database import *
from app.models import *

router = APIRouter()

# Customer: Subscribe to Plans and View Details
@router.post("/subscriptions")
async def subscribe_to_plan(subscription: UserSubscription):
    if await subscriptions_collection.find_one({"user_id": subscription.user_id}):
        raise HTTPException(status_code=400, detail="User already subscribed.")
    plan = await plans_collection.find_one({"name": subscription.plan_name})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    subscription.usage = {api: 0 for api in plan["usage_limits"].keys()}
    await subscriptions_collection.insert_one(subscription.dict())
    return {"message": "Subscription created successfully.", "subscription": subscription}

@router.get("/subscriptions/{user_id}")
async def view_subscription(user_id: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    return convert_id(subscription)

@router.get("/subscriptions/{user_id}/usage")
async def view_usage(user_id: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    return subscription["usage"]

@router.put("/subscriptions/{user_id}")
async def modify_user_plan(user_id: str, plan_name: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    plan = await plans_collection.find_one({"name": plan_name})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    subscription["plan_name"] = plan_name
    subscription["usage"] = {api: 0 for api in plan["usage_limits"].keys()}
    await subscriptions_collection.update_one({"user_id": user_id}, {"$set": subscription})
    return {"message": "Subscription plan updated successfully."}