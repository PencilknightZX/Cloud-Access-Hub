from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from app.managed_apis import router as managed_apis_router
from app.models import *
from app.database import *

app = FastAPI()

# Register Managed APIs
app.include_router(managed_apis_router)

# Admin: Manage Subscription Plans
@app.get("/plans/{plan_name}")
async def get_plan(plan_name: str):
    plan = await plans_collection.find_one({"name": plan_name})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {"Plan" : convert_id(plan)}

@app.post("/plans")
async def create_plan(plan: SubscriptionPlan):
    if await plans_collection.find_one({"name": plan.name}):
        raise HTTPException(status_code=400, detail="Plan already exists.")
    await plans_collection.insert_one(plan.dict())
    return {"message": "Plan created successfully.", "plan": plan}

@app.put("/plans/{plan_name}")
async def modify_plan(plan_name: str, updated_plan: SubscriptionPlan):
    result = await plans_collection.update_one({"name": plan_name}, {"$set": updated_plan.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {"message": "Plan updated successfully."}

@app.delete("/plans/{plan_name}")
async def delete_plan(plan_name: str):
    result = await plans_collection.delete_one({"name": plan_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {"message": "Plan deleted successfully."}

# Admin: Manage Permissions
@app.post("/permissions")
async def add_permission(permission: Permission):
    if await permissions_collection.find_one({"name": permission.name}):
        raise HTTPException(status_code=400, detail="Permission already exists.")
    await permissions_collection.insert_one(permission.dict())
    return {"message": "Permission added successfully.", "permission": permission}

@app.put("/permissions/{permission_name}")
async def modify_permission(permission_name: str, updated_permission: Permission):
    result = await permissions_collection.update_one({"name": permission_name}, {"$set": updated_permission.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found.")
    return {"message": "Permission updated successfully."}

@app.delete("/permissions/{permission_name}")
async def delete_permission(permission_name: str):
    result = await permissions_collection.delete_one({"name": permission_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found.")
    return {"message": "Permission deleted successfully."}

# Customer: Subscribe to Plans and View Details
@app.post("/subscriptions")
async def subscribe_to_plan(subscription: UserSubscription):
    if await subscriptions_collection.find_one({"user_id": subscription.user_id}):
        raise HTTPException(status_code=400, detail="User already subscribed.")
    plan = await plans_collection.find_one({"name": subscription.plan_name})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    subscription.usage = {api: 0 for api in plan["usage_limits"].keys()}
    await subscriptions_collection.insert_one(subscription.dict())
    return {"message": "Subscription created successfully.", "subscription": subscription}

@app.get("/subscriptions/{user_id}")
async def view_subscription(user_id: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    return convert_id(subscription)

@app.get("/subscriptions/{user_id}/usage")
async def view_usage(user_id: str):
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found.")
    return subscription["usage"]

@app.put("/subscriptions/{user_id}")
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

# Access Control
@app.get("/access/{user_id}/{api_endpoint}")
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

# Usage Tracking and Limit Enforcement
@app.post("/usage/{user_id}")
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

@app.get("/usage/{user_id}/limit")
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


