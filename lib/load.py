"""
Funciones para carga de documentos normativos a una fuente de datos.
"""
# Biblioteca estandar
import json
import os

from lib import db
from lib.nlputils import normalize_sentence, vectorize, Vectorizer

# Numpy
import numpy as np
from sklearn.cluster import KMeans

CLUSTER_FILE = "docs/wv.npy"
MATRIX_FILE = "docs/sm.npy"
NUM_CL = 1000  # Number of clusters


def _iterar_divisiones_documento(data, id_documento):
    lvl = data.get("level", "").lower()
    for it in data.get("items", []):
        texto = it.get("text")
        enum = it.get("enum")

        # Crear representacion vectorizada del texto
        texto_normalizado = normalize_sentence(texto)

        # Crear representacion vectorial
        vector, idxs = Vectorizer.vectorize_text(texto_normalizado)

        # Cargar la division estructural a la BD
        id_div_est = db.create_structural_division(
            id_level=lvl, text=texto, id_document=id_documento, enumeration=enum, vector=vector
        )
        if id_div_est is None:
            raise ValueError(
                f"error al crear una division estructural:\n\tDocumento:{id_documento}\n\tNivel:{lvl}\n\tTexto:{texto}"
            )

        # Asociar la division estructural al los clusters
        for idx in idxs:
            db.create_structural_division_words(id_div_est, idx)

        content = it.get("content")
        if content:
            _iterar_divisiones_documento(content, id_documento)


def cargar_vectores(fname):
    # Cargar los lemas
    if not os.path.exists(CLUSTER_FILE):
        print("Cargando lemas...")
        lemas = set()
        with open(fname, encoding="utf8") as f:
            for linea in f:
                lema, _ = linea.split()
                lemas.add(lema)
        lema_muestra = next(iter(lemas))
        vector_muestra = vectorize(lema_muestra)
        resultados = np.zeros((len(lemas), vector_muestra.shape[0]))

        for i, l in enumerate(lemas):
            resultados[i] = vectorize(l)

        print("Calculando clusters...")
        kmeans = KMeans(n_clusters=1000).fit(resultados)
        cc = kmeans.cluster_centers_
        with open(CLUSTER_FILE, "wb") as f:
            np.save(f, cc)
        Vectorizer.clusters = cc
    else:
        print("El archivo de clusters ya existe.")
        Vectorizer.load_clusters_from_file(CLUSTER_FILE)

    # Cargar las similitudes
    if not os.path.exists(MATRIX_FILE):
        print("Calculando matriz de similitud")
        Vectorizer.calculate_cluster_similarities()
        with open(MATRIX_FILE, "wb") as f:
            np.save(f, Vectorizer.matrix)
    else:
        print("El archivo que contiene la matriz ya existe.")
        Vectorizer.load_similarities_from_file(MATRIX_FILE)

    # Guardar instancias de cluster_palabra
    print("Guardando instancias de cluster_palabra")
    for i, cluster in enumerate(Vectorizer.clusters):
        db.create_word_cluster(i, cluster)

    print("Guardando similitudes de clusters")
    # TODO: Guardar similitudes en BD

def cargar_documento(fname):
    if not fname.endswith(".json"):
        raise ValueError(f"archivo {fname} tiene extension de archivo invalido.")
    with open(fname) as input_file:
        data = json.load(input_file)

    # Crear instancia en tabla `documento`
    fname_sin_ext = fname[: fname.rfind(".json")]
    nombre_documento = os.path.basename(fname_sin_ext)
    db.create_legal_document(nombre_documento)

    # Crear instancias de division estructural
    _iterar_divisiones_documento(data, nombre_documento)
