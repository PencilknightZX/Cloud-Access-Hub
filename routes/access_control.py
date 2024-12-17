from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.database import *
from app.models import *

router = APIRouter()

# Access Control
@router.get("/access/{user_id}/{api_endpoint}")
async def check_access(user_id: str, api_endpoint: str):
    # Ensure API endpoint starts with '/'
    if not api_endpoint.startswith("/"):
        api_endpoint = f"/{api_endpoint}"

    # Fetch user subscription
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")

    # Fetch user's plan
    plan = await plans_collection.find_one({"name": subscription["plan_name"]})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")

    # Retrieve the usage limits
    usage_limits = plan.get("usage_limits", {})
    if api_endpoint not in usage_limits:
        raise HTTPException(status_code=403, detail="Access denied.")

    usage_limit = int(usage_limits[api_endpoint])
    usage = subscription.get("usage", {})
    current_usage = int(usage.get(api_endpoint, 0))

    if current_usage >= usage_limit:
        raise HTTPException(status_code=403, detail="Usage limit exceeded.")

    return {"message": "Access granted.", "current_usage": current_usage, "limit": usage_limit}