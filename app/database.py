from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

mongoURI = os.getenv("MONGO_DB_URI")

mongodb_client = AsyncIOMotorClient(mongoURI)
db = mongodb_client['Access_Manager']

subscriptions = db["subscription_plan"]
permissions = db["permissions"]
users = db["users"]