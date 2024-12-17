from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

mongoURI= os.getenv('MONGO_URI')

# MongoDB Setup
client = AsyncIOMotorClient(mongoURI)
db = client.CloudDB

# Collections
permissions_collection = db.permissions
plans_collection = db.plans
subscriptions_collection = db.subscriptions