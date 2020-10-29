# Milo

A legal information assistant bot for ESCOM. 🤖

## Requirements

It is very important to use **Python 3.6.8** due to a strict dependency with Rasa's own dependencies. This may be done using [pyenv](https://github.com/pyenv/pyenv)


## Installation

It is highly recommended to use a virtual environment

```sh
# Activate the virtual environment
source $VENV_PATH/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Installing the language model for Spanish

```bash
python -m spacy download es_core_news_md    
```

### Training the model

Next, Rasa needs to train the model.

```sh
cd rasa
rasa train
```

## Running the bot

```sh
rasa run --cors "*"
```

## (Deprecated) way of running the bot

```sh
# Run the HTTP server on http://localhost:5005
rasa run -m models --enable-api --cors "*"
```

Action server

```sh
# Run the Action server http://localhost:5055
rasa run actions
```