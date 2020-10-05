"""Data source access module."""

from typing import Dict

import pymongo

DB_NAME = "LegalDocs"


def _get_client():
    return pymongo.MongoClient(
        "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false"
    )


def get_division_levels() -> Dict[str, str]:
    client = _get_client()
    db = client[DB_NAME]
    return {
        doc.get("nombre_division"): doc.get("_id")
        for doc in db["NivelDivision"].find({})
        if "nombre_division" in doc
    }


def insert_structural_division(id_level, id_document, enumeration, text):
    client = _get_client()
    db = client[DB_NAME]
    db["DivisionEstructural"].insert_one(
        {
            "id_nivel": id_level,
            "id_document": id_document,
            "numeracion": enumeration,
            "texto": text,
        }
    )


def create_legal_document(document_name):
    client = _get_client()
    db = client[DB_NAME]
    return db["Documento"].insert_one(
        {"nombre_documento": document_name}).inserted_id


if __name__ == "__main__":
    print(get_division_levels())
