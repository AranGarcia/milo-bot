#!/usr/bin/env python3

import argparse
import os

from lib.load import cargar_documento, cargar_vectores

parser = argparse.ArgumentParser(
    description="Script de carga de documentos normativos estructurados a la base de conocimiento"
)
parser.add_argument(
    "--lemas_txt",
    help="Archivo que contiene la lista de palabras con sus respectivos lemas.",
    default="docs/lemmatization-es.txt",
    required=False,
)
parser.add_argument(
    "--dir_json",
    help="Directorio que contiene documentos normativos en formato JSON.",
    default="docs/json/",
    required=False,
)

args = parser.parse_args()

# Calculo de vectores utilizando el arcihvo con los lemas
cargar_vectores(args.lemas_txt)

# Si no existe el directorio, termina la ejecucion
if not os.path.exists(args.dir_json):
    print(f"El directorio '{args.dir_json}' no existe.")
    exit(1)

print(f"Cargando archivos del directorio {args.dir_json}...\n")
for d in os.listdir(args.dir_json):
    print(f"- {d}")
    fname = f"{os.path.realpath(args.dir_json)}/{d}"
    cargar_documento(fname)
