#!/usr/bin/env python
import os
import sys

import numpy as np
import spacy

# HACK: Agregar biblioteca en la raiz del proyecto para importar `lib`.
PROJ_DIR = os.path.realpath(f"{os.path.dirname(os.path.realpath(__file__))}/..")
sys.path.append(PROJ_DIR)
from lib.nlputils import cosine_similarity, similarity, vectorize  # noqa
from lib.db import retrieve_words  # noqa

nlp = spacy.load("es_core_news_lg")


IDXS, VOCAB, VECTORS = retrieve_words()

print("Probando integreidad de las palabras en BD...")
assert IDXS.shape[0] == VOCAB.shape[0] == VECTORS.shape[0]

print("Comparando vector de palabras con su texto...")
for w, v in zip(VOCAB, VECTORS):
    vi = vectorize(str(w))
    sim = v.dot(vi) / (np.linalg.norm(v) * np.linalg.norm(vi))
    assert sim >= 0.9999

test_words = (
    ("rallar", "dañar"),
    ("banca", "propiedad"),
    ("director", "personal"),
    ("rallar", "director"),
    ("propiedad", "director"),
    ("trabajar", "vacaciones"),
    ("consejo", "vacaciones"),
    ("instituto", "IPN"),
)

print("Probando similitudes entre palabras:")
for tw_1, tw_2 in test_words:
    print(f"Palabras: {tw_1}, {tw_2}")

    t1 = nlp(tw_1)
    t2 = nlp(tw_2)
    q = t1.vector
    v = t2.vector

    # Matriz de similitud
    s = (q.dot(v)) / (np.linalg.norm(q) * np.linalg.norm(v))

    print(f"\tsimilitud: {s}\n\tspacy:     {t1.similarity(t2)}")
