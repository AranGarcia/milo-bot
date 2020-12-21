import numpy as np
import spacy

# Carga del modelo linguistico en espanol
nlp = spacy.load("es_core_news_md")


class Vectorizer:
    clusters = None

    @classmethod
    def vectorize_text(cls, text):
        if cls.clusters is None:
            raise ValueError("clusters not initialized")

        # Get number of clusters
        n_cl = cls.clusters.shape[0]

        # TODO: Change Cluster definition in DB to take column index in vector
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
