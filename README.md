# Milo

Chatbot para extraccion de documentos normativos para ESCOM. 🤖

##  Tabla de Contenido <!-- omit in toc -->

- [Milo](#milo)
  - [Instalación](#instalación)
    - [Requerimientos y Dependencias](#requerimientos-y-dependencias)
    - [Entrenando el modelo](#entrenando-el-modelo)
    - [Preparando el contenedor](#preparando-el-contenedor)
  - [Ejecutando el servicio](#ejecutando-el-servicio)
  - [Prubeas](#prubeas)


## Instalación

### Requerimientos y Dependencias

Es muy importante usar la version **3.6.8** debido a una dependencia estricta con las propias dependencias de Rasa. Esto se puede hacer utilizando [pyenv](https://github.com/pyenv/pyenv).

```sh
# Se recomienda utilizar un entorno virtual.
source $VENV_PATH/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Instalaer modelo lingüístico en español
python -m spacy download es_core_news_md    
```

### Entrenando el modelo

```sh
cd rasa
rasa train
```

### Preparando el contenedor

```bash
docker-compose build
docker network create interpreter_net
```

## Ejecutando el servicio

```bash
docker-compose up
```

## Prubeas

Se podría preguntar las siguientes consultas al bot.

- ¿Cuáles son los requisitos para ingresar?
- ¿Que reglamentos hablan sobre la movilidad academica?
- ¿Que pasa si tengo inconformidades?
- ¿Que pasa si estoy en situación irregular?
