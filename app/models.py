from pydantic import BaseModel
from typing import List, Dict, Optional
from bson import ObjectId

# Data Models
class Permission(BaseModel):
    name: str
    api_endpoint: str
    description: Optional[str]

class SubscriptionPlan(BaseModel):
    name: str
    description: Optional[str]
    permissions: List[str]
    usage_limits: Dict[str, int]

class UserSubscription(BaseModel):
    user_id: str
    plan_name: str
    usage: Dict[str, int]

# Helper Function: Convert MongoDB ObjectId to String
def convert_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc