"""
Funciones para carga de documentos normativos a una fuente de datos.
"""
# Biblioteca estandar
import json
import os

from lib import db, nlputils

# Numpy
import numpy as np
from sklearn.cluster import KMeans

CLUSTER_FILE = "docs/wv.npy"


def _iterar_divisiones_documento(data, id_documento):
    lvl = data.get("level", "").lower()
    for it in data.get("items", []):
        texto = it.get("text")
        enum = it.get("enum")

        # Crear representacion vectorizada del texto
        texto_normalizado = nlputils.normalize_sentence(texto)

        # Cargar la division estructural a la BD
        indices = nlputils.Vectorizer.vectorize_text(texto_normalizado)
        id_div_est = db.create_structural_division(
            id_level=lvl,
            text=texto,
            id_document=id_documento,
            enumeration=enum,
        )
        if id_div_est is None:
            raise ValueError(
                f"error al crear una division estructural:\n\tDocumento:{id_documento}\n\tNivel:{lvl}\n\tTexto:{texto}"
            )

        # Asociar la division estructural al los clusters
        for idx in indices:
            db.create_structural_division_words(id_div_est, idx)

        content = it.get("content")
        if content:
            _iterar_divisiones_documento(content, id_documento)


def cargar_vectores(fname):
    # Cargar los lemas
    lemas = set()
    with open(fname, encoding="utf8") as f:
        for linea in f:
            lema, _ = linea.split()
            lemas.add(lema)
    lema_muestra = next(iter(lemas))
    vector_muestra = nlputils.vectorize(lema_muestra)
    resultados = np.zeros((len(lemas), vector_muestra.shape[0]))

    if not os.path.exists(CLUSTER_FILE):
        print("Creando lemas...")
        for i, l in enumerate(lemas):
            resultados[i] = nlputils.vectorize(l)

        print("Calculando clusters...")
        kmeans = KMeans(n_clusters=1000).fit(resultados)
        cc = kmeans.cluster_centers_
        with open(CLUSTER_FILE, "wb") as f:
            np.save(f, cc)
    else:
        print("El archivo de clusters ya existe.")
        cc = np.load(CLUSTER_FILE)

    # Guardar instancias de cluster_palabra
    print("Guardando instancias de cluster_palabra")
    for cluster in cc:
        db.create_word_cluster(cluster)

    nlputils.Vectorizer.clusters = cc


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
