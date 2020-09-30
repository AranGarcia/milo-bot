from typing import Any, Dict
from pymongo import MongoClient


class DocumentDBClient:
    @classmethod
    def insert_document(cls):
        pass

    @staticmethod
    def get_client(host, port):
        return MongoClient(host, port)


def load_yaml(legal_data: Dict[str, Any]):
    pass


def load_json():
    pass