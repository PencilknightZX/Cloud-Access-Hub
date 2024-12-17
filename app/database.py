from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.managemt_apis

# collections
plans_collection = db.plans
permissions_collection = db.permissions
subscriptions_collection = db.collection
usage_collection = db.usage




