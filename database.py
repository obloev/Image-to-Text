from motor import motor_asyncio

from config import MONGODB_URI

SESSION_NAME = 'image-to-text'


class Database:
    def __init__(self):
        self._client = motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        self.db = self._client[SESSION_NAME]
        self.col = self.db.users

    async def add_user(self, user_id):
        user = {
            'id': user_id,
        }
        await self.col.insert_one(user)

    async def is_user_exist(self, user_id):
        user = await self.col.find_one({'id': user_id})
        return True if user else False

    async def get_users(self):
        users = self.col.find({})
        return users

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def delete_user(self, user_id):
        await self.col.delete_one({'id': user_id})
