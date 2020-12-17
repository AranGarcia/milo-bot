"""
Funciones para carga de documentos normativos a una fuente de datos.
"""
# Biblioteca estandar
import json
import os

from lib import db


def _iterar_divisiones_documento(data, id_documento):
    lvl = data.get("level", "").lower()
    for it in data.get("items", []):
        text = it.get("text")
        enum = it.get("enum")

        # TODO: Vectorizar division estructural

        # Load the document segment into the DB
        db.create_structural_division(
            id_level=lvl,
            id_document=id_documento,
            enumeration=enum,
            text=text,
        )

        content = it.get("content")
        if content:
            _iterar_divisiones_documento(content, id_documento)


def cargar_documento(fname):
    if not fname.endswith(".json"):
        raise ValueError(f"archivo {fname} tiene extension de archivo invalido.")
    with open(fname) as input_file:
        data = json.load(input_file)

    # Crear instancia en tabla `documento`
    fname_sin_ext = fname[: fname.rfind(".json")]
    nombre_documento = os.path.basename(fname_sin_ext)
    db.create_legal_document(nombre_documento)

    # Crear instancias de division estructural
    _iterar_divisiones_documento(data, nombre_documento)
