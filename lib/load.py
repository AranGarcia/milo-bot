"""
Funciones para carga de documentos normativos a una fuente de datos.
"""
# Biblioteca estandar
import json
import os

from lib import db

# Numpy
import numpy as np
import spacy
from sklearn.cluster import KMeans

# Carga del modelo linguistico en espanol
nlp = spacy.load("es_core_news_md")


def _iterar_divisiones_documento(data, id_documento):
    lvl = data.get("level", "").lower()
    for it in data.get("items", []):
        text = it.get("text")
        enum = it.get("enum")

        # TODO: Vectorizar division estructural

        # Load the document segment into the DB
        db.create_structural_division(
            id_level=lvl,
            id_document=id_documento,
            enumeration=enum,
            text=text,
        )

        content = it.get("content")
        if content:
            _iterar_divisiones_documento(content, id_documento)


def cargar_vectores(fname):
    lemas = set()
    with open(fname, encoding="utf8") as f:
        for linea in f:
            lema, _ = linea.split()
            lemas.add(lema)
    lema_muestra = next(iter(lemas))
    vector_muestra = nlp(lema_muestra).vector
    resultados = np.zeros((len(lemas), vector_muestra.shape[0]))

    cluster_file = "docs/wv.npy"
    if not os.path.exists(cluster_file):
        print("Creando lemas...")
        for i, l in enumerate(lemas):
            resultados[i] = nlp(l).vector

        print("Calculando clusters...")
        kmeans = KMeans(n_clusters=1000).fit(resultados)
        cc = kmeans.cluster_centers_
        with open(cluster_file, "wb") as f:
            np.save(f, cc)
    else:
        print("El archivo de clusters ya existe.")
        cc = np.load(cluster_file)

    for cluster in cc:
        db.create_word_cluster(cluster)


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
