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
from lib.nlputils import normalize_sentence, WordSpace  # noqa
from lib.db import retrieve_struct_div_by_ids  # noqa


def test_similarity(q, n=5):
    assert q.ndim == 1

    # Oraciones en forma binaria (binary sentences)
    bs = WordSpace.binary_vectors
    # Matriz de similitud
    W = WordSpace.smatrix

    sims = np.apply_along_axis(
        lambda s: (q.dot(W).dot(s)) / (np.linalg.norm(q) * np.linalg.norm(s)), axis=1, arr=bs
    )

    assert bs.shape[0] == sims.shape[0]

    sd_ids = sims.argsort()[-n:]
    return sims[sd_ids], tuple(int(i) for i in sd_ids)


def test_bv_indices(arr, idxs):
    """Verifica indices en el vector binario.

    Dado los indices `idxs`, esta funcion prueba que contenga valores en 1, mientras que los demas
    indices contengan 0.
    """
    return np.all(arr[idxs] == 1) and np.all(np.delete(arr, idxs) == 0)


def test_cases(text: str) -> None:
    """Funcion de prueba de un texto."""
    norm_text = normalize_sentence(text)
    print("\t[texto]")
    print(f"\t- normalizacion: {norm_text}")

    vb, idxs = WordSpace.bvectorize_idxs(norm_text)
    r = test_bv_indices(vb, idxs)
    print("\n\t[vector binario]")
    print("\t- consistencia del vector binario:", r)
    print("\t- dimension:", vb.shape)
    print("\t- clusters:", ", ".join(str(i) for i in idxs))

    sims, de_ids = test_similarity(vb)
    reglamentos = retrieve_struct_div_by_ids(de_ids, "id_nivel, numeracion, id_documento, texto")
    assert len(sims) == len(de_ids) == len(reglamentos)
    print("\n\t[similitud]")
    for s, i, r in zip(sims, de_ids, reglamentos):
        print(f"\t\t- ID: {i}, SIM: {s}")
        print(f"\t\t  {r[2]} {r[0]} {r[1]}")


print("Cargando vectores, clusters y matriz...")
WordSpace.load_binary_representations()
WordSpace.load_clusters_from_file("docs/wv.npy")
WordSpace.load_similarities_from_file("docs/sm.npy")

print("Probando generacion de vectores binarios...")
txt = [
    "baja temporal",
    "consejo tecnico consultivo",
    "rallar bancas del salón",
    (
        "El director general, escuchando la opinión de las academias y colegios de profesores, "
        "determinará las condiciones, requisitos y procedimientos a los que se sujetará el "
        "otorgamiento de la equivalencia o la revalidación de estudios."
    ),
]

for t in txt:
    print(f"'{t}':")
    test_cases(t)
    print()
