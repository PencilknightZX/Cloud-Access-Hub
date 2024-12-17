from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.managed_apis import router as managed_apis_router
from routes.manage_sub_plans import router as manage_sub_router
from routes.permissions import router as perm_router
from routes.user_sub_handling import router as sub_handling_router
from routes.access_control import router as access_router
from routes.track_and_limit import router as track_router

app = FastAPI()

# 6 Cloud Service APIs
app.include_router(managed_apis_router)

# Admin: Manage Subscription Plans
app.include_router(manage_sub_router)

# Admin: Manage Permissions
app.include_router(perm_router)

# Sub Handling: Subscribe to Plans and View Details 
app.include_router(sub_handling_router)

# Access Control
app.include_router(access_router)

# Usage Tracking and Limit Enforcement
app.include_router(track_router)



