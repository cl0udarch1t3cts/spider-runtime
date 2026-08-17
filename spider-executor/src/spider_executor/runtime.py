from pymongo import MongoClient

from spider_executor.service import MongoControlService
from spider_executor.settings import Settings


def create_control(settings: Settings) -> MongoControlService:
    client = MongoClient(settings.mongodb_uri, serverSelectionTimeoutMS=5000)
    service = MongoControlService(client[settings.mongodb_database])
    service.ensure_indexes()
    return service
