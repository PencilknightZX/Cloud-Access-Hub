from fastapi import APIRouter, HTTPException
from database import subscriptions, users
from typing import Dict
from bson import ObjectId

# Create the main router for Subscription Plan APIs
router = APIRouter()

# ROUTE: @subscription-plan/

# Create Plan: For Admins to create a subscription plan
@router.get("/")
async def get_plans():
    plans = []
    async for plan in subscriptions.find():
        # Convert ObjectId to string to make it serializable
        plan["_id"] = str(plan["_id"])
        plans.append(plan)
        
    return plans

# Create Plan: For Admins to create a subscription plan
@router.post("/")
async def create_plan(request: Dict):
    id = ObjectId(request.get("userId"))
    
    if not id:
        raise HTTPException(status_code=400, detail="No ID provided")
    
    user = await users.find_one({"_id": id})
    
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    if user.get("isAdmin") != 1:
        raise HTTPException(status_code=401, detail="Not an Admin" )
    
    if all(key in request for key in ["planName", "description", "apiPerms", "limit"]):
        fields = {
            "plan_name": request.get("planName"),
            "description": request.get("description"),
            "api_perms" : request.get("apiPerms"),
            "usage_lim" : request.get("limit")            
        }
        
        resp = await subscriptions.insert_one(fields)
        
        if not resp.inserted_id:
            raise HTTPException(status_code=500, detail="Failed to Insert")
        
        return {"message": "Subscription plan created successfully", "plan_id": str(resp.inserted_id)}


    raise HTTPException(status_code=400, detail="Missing Parameter")
        

# Modify Plan: For Admins to modify existing subscription plans
@router.put("/")
async def modify_plan():
    return {"message": "File Storage API is working!"}

# Delete Plan: For Admins to delete existing subscription plans
@router.delete("/{id}")
async def delete_plan(id: int):
     
    return {"message": "File Storage API is working!"}
