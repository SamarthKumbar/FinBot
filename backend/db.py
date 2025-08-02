from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DETAILS = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME", "balance_sheet_db")

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client[DB_NAME]


user_collection = db.get_collection("users")
company_collection = db.get_collection("companies")
balance_sheet_collection = db.get_collection("balance_sheets")
