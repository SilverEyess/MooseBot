from motor.motor_asyncio import AsyncIOMotorClient


class MooseDb:

    def __init__(self):
        self.client = AsyncIOMotorClient()
        self.db = self.client.MooseBot
        # TODO finish
