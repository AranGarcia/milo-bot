import spacy

# Carga del modelo linguistico en espanol
nlp = spacy.load("es_core_news_md")


def normalize_sentence(sentence):
    norm_sent = nlp(sentence.lower())
    token_list = [token.lemma_ for token in norm_sent if not token.is_stop and not token.is_punct]
    return " ".join(token_list)


def vectorize(text):
    return nlp(text).vector
