#!/usr/bin/env python
"""
Pruebas de afirmacion sobre la busqueda de conceptos.
"""

# HACK: Agregar biblioteca en la raiz del proyecto para importar `lib`.
import os

PROJ_DIR = os.path.realpath(f"{os.path.dirname(os.path.realpath(__file__))}/..")

import sys  # noqa

sys.path.append(PROJ_DIR)


from lib.nlputils import WordSpace  # noqa


print("Pruebas de busqueda de conceptos...")
WordSpace.load_binary_representations()
WordSpace.load_clusters_from_file("docs/wv.npy")
WordSpace.load_similarities_from_file("docs/sm.npy")
