from typing import Tuple

import numpy as np
import spacy

from lib.db import retrieve_words

# Carga del modelo linguistico en espanol
nlp = spacy.load("es_core_news_lg")


def cosine_similarity(v1: np.array, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


class WordSpace:
    indexes = None
    vectors = None
    vocabulary = None

    @classmethod
    def load(cls) -> None:
        idxs, voc, vec = retrieve_words()

        if not (idxs.shape[0] == voc.shape[0] == vec.shape[0]):
            raise ValueError("inconsistent shape of vocabulary within data source")

        cls.indexes, cls.vocabulary, cls.vectors = idxs, voc, vec

    @classmethod
    def search(cls, text: str, threshold: float = 0.7) -> Tuple[np.array, np.array]:
        wv = vectorize(text)

        sims = np.apply_along_axis(
            func1d=lambda v: wv.dot(v) / (np.linalg.norm(wv) * np.linalg.norm(v)),
            axis=1,
            arr=cls.vectors,
        )

        sims_idxs = sims.argsort()[-10:]
        w_ids = np.argwhere(sims[sims_idxs] >= threshold)
        return sims[sims_idxs][w_ids], tuple(int(cls.indexes[i]) for i in sims_idxs[w_ids])


def normalize_sentence(sentence: str):
    norm_sent = nlp(sentence)
    token_list = [token.lemma_ for token in norm_sent if not token.is_stop and not token.is_punct]
    return " ".join(token_list)


def vectorize(w: str):
    return nlp(w).vector


def similarity(w1: str, w2: str) -> float:
    if not isinstance(w1, str) or not isinstance(w2, str):
        raise ValueError("both words must be strings")
    doc = nlp(f"{w1} {w2}")
    return doc[0].similarity(doc[1])
