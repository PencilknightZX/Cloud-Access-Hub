from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.database import *
from app.models import *

router = APIRouter()

# Admin: Manage Subscription Plans
@router.get("/plans/{plan_name}")
async def get_plan(plan_name: str):
    plan = await plans_collection.find_one({"name": plan_name})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {"Plan" : convert_id(plan)}

@router.post("/plans")
async def create_plan(plan: SubscriptionPlan):
    if await plans_collection.find_one({"name": plan.name}):
        raise HTTPException(status_code=400, detail="Plan already exists.")
    await plans_collection.insert_one(plan.dict())
    return {"message": "Plan created successfully.", "plan": plan}

@router.put("/plans/{plan_name}")
async def modify_plan(plan_name: str, updated_plan: SubscriptionPlan):
    result = await plans_collection.update_one({"name": plan_name}, {"$set": updated_plan.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {"message": "Plan updated successfully."}

@router.delete("/plans/{plan_name}")
async def delete_plan(plan_name: str):
    result = await plans_collection.delete_one({"name": plan_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return {"message": "Plan deleted successfully."}