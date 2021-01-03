"""Funciones de transformacion de archivos."""

import spacy

from lib.legal_structures.base import identify_item
from lib.legal_structures.legal_file import LegalFileStructure


nlp = spacy.load("es_core_news_lg")


def estructurar_documento(fname: str, dir_out: str):
    """Recibe un documento normatvo en formato TXT, lo transforma a JSON y lo escribe en el directorio
    de salida `dir`."""
    if not fname.endswith(".txt"):
        raise ValueError(f"archivo {fname} tiene extension de archivo invalido.")

    lfs = LegalFileStructure()
    paragraphs = []
    with open(fname) as input_file:
        for line in input_file:
            # Remove trailing whitespace.
            line = line.strip()

            # Parse all paragraphs as a single item
            if line != "":
                paragraphs.append(line)
            else:
                text = "\n".join(paragraphs)
                paragraphs.clear()
                item = identify_item(text)
                if item:
                    lfs.add_item(item)

    fname_without_txt = fname[: fname.rfind(".txt")]
    return lfs.write_file(fname_without_txt, dir_out)
