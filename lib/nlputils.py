import numpy as np
import spacy

# Carga del modelo linguistico en espanol
nlp = spacy.load("es_core_news_md")


def _cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


class WordSpace:
    clusters = None
    matrix = None

    @classmethod
    def load_clusters_from_file(cls, fname):
        cls.clusters = np.load(fname)

    @classmethod
    def load_similarities_from_file(cls, fname):
        cls.matrix = np.load(fname)

    @classmethod
    def calculate_cluster_similarities(cls):
        if cls.clusters is None:
            raise ValueError("clusters not initialized")

        md = cls.clusters.shape[0]  # Dimension of the square matrix
        cls.matrix = np.zeros((md, md))
        for idx in np.ndindex(md, md):
            cls.matrix[idx] = _cosine_similarity(cls.clusters[idx[0]], cls.clusters[idx[1]])

    @classmethod
    def vectorize_text(cls, text):
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

        return vector, indexes


def normalize_sentence(sentence):
    norm_sent = nlp(sentence.lower())
    token_list = [token.lemma_ for token in norm_sent if not token.is_stop and not token.is_punct]
    return " ".join(token_list)


def vectorize(text):
    return nlp(text).vector
