"""
Funciones para carga de documentos normativos a una fuente de datos.
"""
# Biblioteca estandar
import json
import os

from lib import db

import spacy

nlp = spacy.load("es_core_news_lg")


# Cache de palabras que han sido registradas en el vocabulario
CACHE = {}


def _iterar_divisiones_documento(data, id_documento):
    lvl = data.get("level", "").lower()
    for it in data.get("items", []):
        texto = it.get("text")
        enum = it.get("enum")

        # Cargar la division estructural a la BD
        id_div_est = db.create_structural_division(
            id_level=lvl, text=texto, id_document=id_documento, enumeration=enum
        )
        if id_div_est is None:
            raise ValueError(
                f"error al crear una division estructural:\n\tDocumento:{id_documento}\n\tNivel:{lvl}\n\tTexto:{texto}"
            )

        idxs = []
        doc = nlp(texto)
        for tok in doc:
            if not tok.has_vector or tok.is_oov:
                continue
            elif not tok.is_stop and not tok.is_punct:
                stripped_tok = tok.text.strip()
                if stripped_tok == "":
                    continue

                _id = db.create_word(stripped_tok, tok.vector)
                if _id is None:
                    if stripped_tok in CACHE:
                        _id = CACHE[stripped_tok]
                    else:
                        raise ValueError(
                            f"error al cargar '{tok.text}' del {id_documento} {lvl} {enum} "
                        )
                else:
                    CACHE[stripped_tok] = _id
                idxs.append(_id)

        # Asociar la division estructural al los clusters
        for idx in idxs:
            db.create_structural_division_words(id_div_est, idx)

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
