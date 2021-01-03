#!/usr/bin/env python
"""
Pruebas de afirmacion sobre la busqueda de conceptos.
"""
import os
import sys

import numpy as np

# HACK: Agregar biblioteca en la raiz del proyecto para importar `lib`.
PROJ_DIR = os.path.realpath(f"{os.path.dirname(os.path.realpath(__file__))}/..")
sys.path.append(PROJ_DIR)
from lib.nlputils import cosine_similarity, similarity, vectorize  # noqa
from lib.db import retrieve_words, retrieve_struct_div_by_word_id  # noqa


IDXS, VOCAB, VECTORS = retrieve_words()


def test_similarity(w, thres=0.5):
    wv = vectorize(w)
    sims = np.apply_along_axis(
        func1d=lambda v: wv.dot(v) / (np.linalg.norm(wv) * np.linalg.norm(v)),
        axis=1,
        arr=VECTORS,
    )

    sd_ids = np.argwhere(sims >= thres)
    return sims[sd_ids], tuple(int(IDXS[i]) for i in sd_ids)


def test_cases(text: str) -> None:
    """Funcion de prueba de un texto."""
    print(f"\t[texto]: {text}")

    sims, de_ids = test_similarity(text)
    for s, i in zip(sims, de_ids):
        sd = retrieve_struct_div_by_word_id((i,))[0]
        print(f"\t\t- ID: {i}, SIM: {s}")
        print(f"\t\t  Doc: {sd[1]} {sd[2]} {sd[3]}")


if __name__ == "__main__":
    txt = [
        # "credencial",
        # "falsificar",
        # "intercambio",
        # "movilidad",
        "rallar",
        "propiedad",
    ]
    for t in txt:
        print(f"'{t}':")
        test_cases(t)
        print()
