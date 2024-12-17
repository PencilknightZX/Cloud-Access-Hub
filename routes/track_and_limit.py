from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.database import *
from app.models import *

router = APIRouter()

# Usage Tracking and Limit Enforcement
@router.post("/usage/{user_id}")
async def track_api_usage(user_id: str, api_endpoint: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    plan = await plans_collection.find_one({"name": subscription["plan_name"]})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    if api_endpoint not in plan["usage_limits"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    usage = subscription.get("usage", {})
    if usage.get(api_endpoint, 0) >= plan["usage_limits"][api_endpoint]:
        raise HTTPException(status_code=403, detail="Usage limit exceeded.")
    usage[api_endpoint] = usage.get(api_endpoint, 0) + 1
    await subscriptions_collection.update_one({"user_id": user_id}, {"$set": {"usage": usage}})
    return {"message": "API usage tracked successfully.", "usage": usage}

@router.get("/usage/{user_id}/limit")
async def check_limit_status(user_id: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    plan = await plans_collection.find_one({"name": subscription["plan_name"]})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    limits = {api: {
        "used": subscription["usage"].get(api, 0),
        "limit": plan["usage_limits"].get(api, 0)
    } for api in plan["usage_limits"].keys()}
    return limits