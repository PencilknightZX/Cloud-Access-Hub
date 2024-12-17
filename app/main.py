from fastapi import FastAPI
from routes.managed_apis import router as managed_apis_router
from routes.subscription_plan import router as subscription_plan_router
from routes.permission_management import router as permissions_router

app = FastAPI()

# Include the grouped APIs
app.include_router(managed_apis_router, prefix="/managed-apis", tags=["Managed APIs"])

app.include_router(subscription_plan_router, prefix="/subscription-plan", tags=["Subscriptions"])

app.include_router(permissions_router, prefix="/permissions", tags=["Permissions"])

