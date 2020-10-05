"""
Preprocessing and data preparation class for the legal documents.
"""

# Standard library
import json
from os.path import basename
from typing import List

# External packaged
from unidecode import unidecode

# from yaml import Loader, load


# DB Acces
import db

# Legal structure
from legal_structures.base import identify_item
from legal_structures.legal_file import LegalFileStructure

# from word_vectors import load_lemmas

LEVELS = db.get_division_levels()
VALID_DOC_FORMATS = {"json", "yaml"}


def structurize_txt(fname: str, output_format: str = "json"):
    """Structures a legal document in TXT format into a YAML with
    structure.
    """

    if not fname.endswith(".txt"):
        raise ValueError(f"file {fname} has invalid format.")

    if output_format not in VALID_DOC_FORMATS:
        raise ValueError(f"invalid output format {output_format}.")

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
    return lfs.write_file(fname_without_txt, file_format=output_format)


def structurize_txt_list(flist: List[str], output_format: str = "json"):
    return [structurize_txt(fitem) for fitem in flist]


def iter_depth_document(obj, id_document):
    lvl = obj.get("level", "").lower()
    if lvl not in LEVELS:
        raise ValueError(f"invalid document level: {lvl}")

    for it in obj.get("items", []):
        text = it.get("text")
        enum = it.get("enum")

        print(f"Inserting {lvl} {enum} in {id_document}")
        db.insert_structural_division(
            id_level=LEVELS[lvl],
            id_document=id_document,
            enumeration=enum,
            text=text,
        )

        content = it.get("content")
        if content:
            iter_depth_document(content, id_document)


def load_structured_legal_doc(fname):
    # First validate that the file is in a valid format
    extension_format = fname[(fname.rfind(".") + 1) :]
    if extension_format not in VALID_DOC_FORMATS:
        raise ValueError(f"invalid format {fname}.")

    with open(fname) as input_file:
        if extension_format == "json":
            data = json.load(input_file)
        elif extension_format == "yaml":
            raise NotImplementedError("YAML not yet integrated.")
        else:
            raise ValueError(f"unknown extension <{extension_format}>")

        # Create Document instance in DB
        id_document = db.create_legal_document(basename(fname))

        # Iterate over data
        iter_depth_document(data, id_document)


def __load_yaml(fobj):
    return load(fobj, Loader=Loader)

    # @staticmethod
    # def __load_clusters(fname: str, k: int = 10_000):
    #     """Reads a file with lemmas and groups them into 10,000 new cluster centers."""
    #     # First load lemmas
    #     lemmas = load_lemmas(fname)


if __name__ == "__main__":
    """This is just for testing."""
    docs = [
        "/home/aran/projects/atl/shepard.docs/txt/ley-organica.txt",
        "/home/aran/projects/atl/shepard.docs/txt/reglamento-de-titulacion-profesional.txt",
        "/home/aran/projects/atl/shepard.docs/txt/reglamento-general-de-estudios.txt",
        "/home/aran/projects/atl/shepard.docs/txt/reglamento-interno.txt",
    ]

    print("Structuring text files.")
    results = structurize_txt_list(docs)
    print(f"Loading {len(results)} files into the database.")
    for r in results:
        load_structured_legal_doc(r)
