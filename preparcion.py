#!/usr/bin/env python3
"""
Script de preparacion de documentos normativos

Transforma los documentos en formato TXT a un formato estructurado JSON. Este script itera
sobre los archivos de un directorio, transforma el formato y los escribe un directorio destino.
"""

import argparse
import os

from lib.transform import estructurar_documento

parser = argparse.ArgumentParser(
    description="Script de preparacion de documentos normativos de formato TXT a JSON."
)
parser.add_argument(
    "--dir_txt",
    help="Directorio que contiene los archivos de entrada en formtato TXT.",
    default="docs/txt/",
    required=False,
)
parser.add_argument(
    "--dir_sal",
    help="Directorio de salida en donde se escribirán los archivos resultantes en formato JSON.",
    default="docs/json/",
    required=False,
)
args = parser.parse_args()

# Verificacion de directorios de entrada y salida
if not os.path.exists(args.dir_txt):
    print(f"El directorio {args.dir_txt} no existe.")
    exit(1)
elif not os.path.isdir(args.dir_txt):
    print(f"La ruta especificada {args.dir_txt} no es un directorio válido.")
    exit(1)

# Si no existe el directorio de salida, se crea
if not os.path.exists(args.dir_sal):
    try:
        os.makedirs(args.dir_sal)
    except PermissionError:
        print(f"No se pudo crear el archivo destino {args.dir_sal}; error de permisos.")
        exit(1)

print(f"Leyendo archivos del directorio {args.dir_txt}...\n")
for d in os.listdir(args.dir_txt):
    print(f"- {d}")
    fname = f"{os.path.realpath(args.dir_txt)}/{d}"
    try:
        estructurar_documento(fname, args.dir_sal)
    except ValueError as ve:
        print(f"\tOmitiendo archivo: {ve}")
