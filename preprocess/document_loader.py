"""
Preprocessing and data preparation class for the legal documents.
"""

# Standard library
import pickle

# YAML
from yaml import Loader, load

# Preprocessing packages
from legal_structures.base import identify_item
from legal_structures.legal_file import LegalFileStructure
# from word_vectors import load_lemmas


class Preprocessor:
    """File preprocessor class.

    Transforms and structures files in preparation for data loading of the legal files.
    """

    VALID_DOC_FORMATS = {"json", "yaml"}

    # @classmethod
    # def load_data(cls):
    #     """Loads all necessary data for Milo to work.

    #     This method prepares and loads the following data:
    #     - word vectors:
    #     """
    #     cls.__load_clusters()

    @classmethod
    def structurize_txt(cls, fname: str, output_format: str = "json"):
        """Structures a legal document in TXT format into a YAML with structure."""

        if not fname.endswith(".txt"):
            raise ValueError(f"file {fname} has invalid format.")

        if output_format not in cls.VALID_DOC_FORMATS:
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

        fname_without_txt = fname[:fname.rfind(".txt")]
        lfs.write_file(fname_without_txt, file_format=output_format)

    @classmethod
    def load_structured_legal_doc(cls, fname):
        # First validate that the file is in a valid format
        extension_format = fname[(fname.rfind(".") + 1) :]
        if extension_format not in cls.VALID_DOC_FORMATS:
            raise ValueError(f"invalid format {fname}.")

        with open(fname) as input_file:
            if extension_format == "json":
                data = cls.__load_json(input_file)
            else:
                data = cls.__load_yaml(input_file)

    @classmethod
    def __load_json(fobj):
        return pickle.load(fobj)

    @classmethod
    def __load_yaml(fobj):
        return load(fobj, Loader=Loader)

    # @staticmethod
    # def __load_clusters(fname: str, k: int = 10_000):
    #     """Reads a file with lemmas and groups them into 10,000 new cluster centers."""
    #     # First load lemmas
    #     lemmas = load_lemmas(fname)


if __name__ == "__main__":
    docs = [
        "/home/aran/projects/atl/shepard.docs/txt/ley-organica.txt",
        "/home/aran/projects/atl/shepard.docs/txt/reglamento-de-titulacion-profesional.txt",
        "/home/aran/projects/atl/shepard.docs/txt/reglamento-general-de-estudios.txt",
        "/home/aran/projects/atl/shepard.docs/txt/reglamento-interno.txt",
    ]

    results = []
    for d in docs:
        Preprocessor.structurize_txt(d)