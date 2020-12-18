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

        # TODO: Change Cluster definition in DB to take column index in vector
        indexes = set()
        for word in text.split():
            word_vector = nlp(word).vector
            distances = np.linalg.norm(cls.clusters - word_vector, axis=1)
            indexes.add(int(np.argmin(distances)) + 1)
        return indexes


def normalize_sentence(sentence):
    norm_sent = nlp(sentence.lower())
    token_list = [token.lemma_ for token in norm_sent if not token.is_stop and not token.is_punct]
    return " ".join(token_list)

def vectorize(text):
    return nlp(text).vector
