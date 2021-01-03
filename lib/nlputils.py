import numpy as np
import spacy

from lib.db import (
    retrieve_amount_of_clusters,
    retrieve_amount_of_struct_divs,
    retrieve_clusters,
    retrieve_struct_div_words,
)

# Carga del modelo linguistico en espanol
nlp = spacy.load("es_core_news_lg")


def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


class WordSpace:
    binary_vectors = None  # Binary sentences
    clusters = None  # Word clusters
    smatrix = None  # Similarity matrix

    @classmethod
    def load_clusters_from_file(cls, fname):
        cls.clusters = np.load(fname)

    @classmethod
    def load_clusters_from_db(cls):
        clusters_db = retrieve_clusters()
        clusters_db.sort(key=lambda x: x[0])

        cls.clusters = np.zeros((len(clusters_db), nlp.vocab.vectors.shape[1]))
        for idx, cdb in enumerate(clusters_db):
            cls.clusters[idx] = cdb[1]

    @classmethod
    def load_similarities_from_file(cls, fname):
        cls.smatrix = np.load(fname)

    @classmethod
    def load_binary_representations(cls):
        """Builds the binary representation of all sentences in the legal documents."""
        idxs = retrieve_struct_div_words()
        amount = retrieve_amount_of_struct_divs()
        n_clusters = retrieve_amount_of_clusters()
        cls.binary_vectors = np.zeros((amount, n_clusters))

        for idx in idxs:
            cls.binary_vectors[(idx[0] - 1, idx[1])] = 1

    @classmethod
    def calculate_cluster_similarities(cls):
        if cls.clusters is None:
            raise ValueError("clusters not initialized")

        md = cls.clusters.shape[0]  # Dimension of the square matrix
        cls.smatrix = np.zeros((md, md))
        for idx in np.ndindex(md, md):
            cls.smatrix[idx] = cosine_similarity(cls.clusters[idx[0]], cls.clusters[idx[1]])

    @classmethod
    def bvectorize_idxs(cls, text):
        """
        Return the binary vector representation and a set of indexes.py

        The binary vector representation will have a 1 where the word cluster is present and 0
        otherwise. Also, the set of indexes contains the cluster number that is present in the text
        (i.e., indexes where there is a 1).
        """
        if cls.clusters is None:
            raise ValueError("clusters not initialized")

        # Get number of clusters
        n_cl = cls.clusters.shape[0]

        indexes = set()
        for word in text.split():
            word_vector = nlp(word).vector
            distances = np.linalg.norm(cls.clusters - word_vector, axis=1)
            indexes.add(int(np.argmin(distances)))

        vector = np.zeros(n_cl, dtype=np.int8)
        np.put(vector, list(indexes), 1)

        return vector, list(indexes)

    @classmethod
    def bvectorize(cls, text):
        if cls.clusters is None:
            raise ValueError("clusters not initialized")

        # Get number of clusters
        n_cl = cls.clusters.shape[0]
        indexes = set()
        for word in text.split():
            word_vector = nlp(word).vector
            distances = np.linalg.norm(cls.clusters - word_vector, axis=1)
            indexes.add(int(np.argmin(distances)))

        vector = np.zeros(n_cl, dtype=np.int8)
        np.put(vector, list(indexes), 1)

        return vector


def normalize_sentence(sentence):
    norm_sent = nlp(sentence)
    token_list = [token.lemma_ for token in norm_sent if not token.is_stop and not token.is_punct]
    return " ".join(token_list)


def vectorize(w):
    return nlp(w)[0].vector


def similarity(w1: str, w2: str) -> float:
    if not isinstance(w1, str) or not isinstance(w2, str):
        raise ValueError("both words must be strings")
    doc = nlp(f"{w1} {w2}")
    return doc[0].similarity(doc[1])
