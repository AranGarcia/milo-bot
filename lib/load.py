"""
Funciones para carga de documentos normativos a una fuente de datos.
"""
# Biblioteca estandar
import json
import os

from lib.db import create_legal_document


def cargar_documento(fname):
    if not fname.endswith(".json"):
        raise ValueError(f"archivo {fname} tiene extension de archivo invalido.")
    with open(fname) as input_file:
        data = json.load(input_file)

    fname_sin_ext = fname[: fname.rfind(".json")]
    nombre_documento = os.path.basename(fname_sin_ext)
    create_legal_document(nombre_documento)
