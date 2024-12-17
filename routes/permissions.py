from fastapi import FastAPI, HTTPException, Depends, APIRouter
from app.database import *
from app.models import *

router = APIRouter()

# Admin: Manage Permissions
@router.get("/permissions/{permission_name}")
async def get_permission(permission_name: str):
    permission = await permissions_collection.find_one({"name": permission_name})
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found.")
    return {"Permission" : convert_id(permission)}

@router.post("/permissions")
async def add_permission(permission: Permission):
    if await permissions_collection.find_one({"name": permission.name}):
        raise HTTPException(status_code=400, detail="Permission already exists.")
    await permissions_collection.insert_one(permission.dict())
    return {"message": "Permission added successfully.", "permission": permission}

@router.put("/permissions/{permission_name}")
async def modify_permission(permission_name: str, updated_permission: Permission):
    result = await permissions_collection.update_one({"name": permission_name}, {"$set": updated_permission.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found.")
    return {"message": "Permission updated successfully."}

@router.delete("/permissions/{permission_name}")
async def delete_permission(permission_name: str):
    result = await permissions_collection.delete_one({"name": permission_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Permission not found.")
    return {"message": "Permission deleted successfully."}
