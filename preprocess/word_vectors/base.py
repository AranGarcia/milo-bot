"""Word preprocessing functions."""

# Standard library
from typing import List

# Spacy - NLP
import spacy


def load_lemmas(fname: str) -> List[str]:
    """Load lemmas from a file.

    Reads a file of word pairs: the lemma itself and an inflection of the lemma.
    The lemmas are then returned in a sorted list.
    """
    lemmas = set()
    with open(fname, encoding="utf8") as f:
        for line in f:
            lemma, _ = line.split()
            lemmas.add(lemma)

    return sorted(lemmas)

def lemmatize_word(w):
    