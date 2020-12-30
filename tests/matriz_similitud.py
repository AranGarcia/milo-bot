#!/usr/bin/env python3
"""
Pruebas de afirmacion acerca de la matriz de similitud.
"""

# HACK: Agregar biblioteca en la raiz del proyecto para importar `lib`.
import os

PROJ_DIR = os.path.realpath(f"{os.path.dirname(os.path.realpath(__file__))}/..")

import sys  # noqa

sys.path.append(PROJ_DIR)

import numpy as np  # noqa

from lib.nlputils import cosine_similarity  # noqa


MATRIX_FILE = "docs/sm.npy"
CLUSTER_FILE = "docs/wv.npy"


sm = np.load(MATRIX_FILE)

print("- Probando que la matrix sea cuadrada...")
assert sm.shape[0] == sm.shape[1]

print("- Probando que la matriz sea simetrica...")
assert np.allclose(sm, sm.T)

print("- Probando tolerancia de la diagonal (±0.0001)...")
idxs = np.diag_indices(sm.shape[0])
assert np.allclose(sm[idxs], np.ones(sm.shape[0]))

print("\nPruebas adicionales sobre vectores de clusters")

wc = np.load(CLUSTER_FILE)

print("- Verificando calculos de similitud coseno...")
temp = np.zeros(sm.shape)
for idx in np.ndindex(wc.shape[0], wc.shape[0]):
    temp[idx] = cosine_similarity(wc[idx[0]], wc[idx[1]])

assert np.allclose(sm, temp)

print("\nPruebas finalizadas.")
