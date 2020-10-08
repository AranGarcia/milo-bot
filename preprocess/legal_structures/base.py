from enum import Enum
import re


# Load lemma dictionary
ENUMERATION_LEMMAS = dict()
with open("enumeration-lemmas.txt") as f:
    for i, line in enumerate(f):
        words = [w.strip() for w in line.split(maxsplit=1)]
        if len(words) < 2:
            raise ValueError(f"Invalid file: enumeration-lemmas.txt, line {i}.")
        if words[1] in ENUMERATION_LEMMAS:
            raise ValueError(f"Duplicate word: {words [1]}, line {i}.")
        ENUMERATION_LEMMAS[words[1]] = words[0]

ROMAN_NUMERALS = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000,
    "IV": 4,
    "IX": 9,
    "XL": 40,
    "XC": 90,
    "CD": 400,
    "CM": 900,
}


class ItemType(Enum):
    TITULO = 1
    CAPITULO = 2
    SECCION = 3
    ARTICULO = 4


# Patterns
tit_pattern = re.compile(r"^(Título|TÍTULO) (.+?)[ .-]+(.+)$")
cap_pattern = re.compile(r"^(Capítulo|CAPÍTULO) (.+?)[ .-]+(.+?)$")
sec_pattern = re.compile(r"^(Sección|SECCIÓN) (.+?)[ .-]+(.+?)$")
# DOTALL in art_pattern is to match paragraphs
art_pattern = re.compile(r"^(Artículo|ARTÍCULO) (\d+?)[ .-]+(.+)$", re.DOTALL)


def identify_item(text: str) -> ItemType:
    """Identify a string as an item from the document.

    Returns a tuple with the following format:
    (ItemType, enumeration, text)"""
    item_match = tit_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.TITULO, *item_match.groups()[1:])

    item_match = cap_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.CAPITULO, *item_match.groups()[1:])

    item_match = sec_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.SECCION, *item_match.groups()[1:])

    item_match = art_pattern.match(text)
    if item_match:
        return LegalDocItem(ItemType.ARTICULO, *item_match.groups()[1:])

    return None


class LegalDocItem:
    __roman_numeral_regex = re.compile(
        r"^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
    )

    def __init__(self, itemtype, enumeration, text):
        self.itemtype = itemtype

        if enumeration.lower() == "único" or enumeration.lower() == "unico":
            self.enumeration = 1
        else:
            self.enumeration = self.__enumeration_to_int(enumeration)

        if itemtype != ItemType.ARTICULO:
            self.text = text
        else:
            self.text = text.title()

    @classmethod
    def __roman_to_int(cls, roman_numeral_string):
        roman_numeral_string = roman_numeral_string.upper()

        if not cls.__roman_numeral_regex.match(roman_numeral_string):
            return None

        i = 0
        num = 0
        while i < len(roman_numeral_string):
            if (
                i + 1 < len(roman_numeral_string)
                and roman_numeral_string[i : i + 2] in ROMAN_NUMERALS
            ):
                num += ROMAN_NUMERALS[roman_numeral_string[i : i + 2]]
                i += 2
            else:
                # print(i)
                num += ROMAN_NUMERALS[roman_numeral_string[i]]
                i += 1
        return num

    @classmethod
    def __enumeration_to_int(cls, enumeration_string):
        # First try to transform from roman numeral
        num = cls.__roman_to_int(enumeration_string)
        if num is not None:
            return num

        # Transform to lower case
        enumeration_string = enumeration_string.lower()
        for k, v in ENUMERATION_LEMMAS.items():
            break
        if enumeration_string.isdecimal():
            return int(enumeration_string)
        else:
            return int(ENUMERATION_LEMMAS[enumeration_string])
