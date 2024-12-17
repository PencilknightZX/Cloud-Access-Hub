from fastapi import APIRouter

# Create the main router for Permission Management APIs
router = APIRouter()

# ROUTE: @permissions/

# Create Permissions: For Admins to create a Permission
@router.post("/addPermission")
async def create_permissions():
    return {"message": "Route!"}

# Modify Permissions: For Admins to modify existing permissions
@router.put("/modifyPermission")
async def modify_permissions():
    return {"message": "Route!"}

# Delete Permissions: For Admins to delete existing permissions
@router.delete("/deletePermission")
async def delete_permissions():
    return {"message": "Route!"}
