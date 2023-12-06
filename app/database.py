import asyncio
from fastapi import FastAPI
from beanie import init_beanie
from pymongo.server_api import ServerApi
from motor.motor_asyncio import AsyncIOMotorClient
from  . import model
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

origins=["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB configuration
DATABASE_URL = f"mongodb+srv://{settings.database_username}:{settings.database_password}@{settings.cluster_address}/{settings.options}"

client = AsyncIOMotorClient(DATABASE_URL, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
      print(e)

async def main():  
    client = AsyncIOMotorClient(DATABASE_URL)
    database = client.todo
        # Initialize Beanie with Task model
    await init_beanie(database, document_models=[model.Task])
    await init_beanie(database, document_models=[model.User])

if __name__ == "__main__":
    asyncio.run(main())
