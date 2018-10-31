from pymongo import MongoClient


class MooseDb:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.MooseBot
        # TODO finish
