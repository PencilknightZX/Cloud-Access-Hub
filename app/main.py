from fastapi import FastAPI
from routes.managed_apis import router as managed_apis_router

app = FastAPI()

# Include the grouped managed APIs
app.include_router(managed_apis_router, prefix="/managed-apis", tags=["Managed APIs"])


