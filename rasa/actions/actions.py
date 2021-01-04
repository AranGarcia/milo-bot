from difflib import SequenceMatcher
from typing import Any, Dict, List, Text

import numpy as np
from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from lib import db, nlputils


# Override default configuration for pg client
db.PostgresClient.host = "knowledge_base"
db.PostgresClient.port = 5432

# Initialize word space class
nlputils.WordSpace.load()


DOCS = [
    "reglamento interno",
    "reglamento general de estudios",
    "reglamento de titulacion profesional",
    "ley organica",
]

DOC_IDS = [
    "reglamento-interno",
    "reglamento-general-de-estudios",
    "reglamento-de-titulacion-profesional",
    "ley-organica",
]


def _str_sim(a, b):
    return SequenceMatcher(None, a, b).ratio()


def identify_document(doc_name):
    sims = [_str_sim(doc_name.lower(), d) for d in DOCS]
    val, idx = max((val, idx) for (idx, val) in enumerate(sims))
    if val < 0.65:
        return -1
    return idx


def format_title(title: str) -> str:
    return title.replace("-", " ").title()


def sd_html(doc_name, level, enumeration, text):
    """Format document text with HTML."""
    return f"<b>{level} {enumeration} del {doc_name}</b>. {text}"


class ActionExtractArticle(Action):
    def name(self) -> Text:
        return "action_extract_article"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        doc = tracker.get_slot("documento")
        niv_est = tracker.get_slot("nivel_estructural")
        niv = tracker.get_slot("nivel")

        if doc is None:
            # No document provided in message
            dispatcher.utter_message(text="¿De qué documento necesitas extraer informacion?")
        else:
            doc_idx = identify_document(doc)
            if doc_idx < 0:
                # Document not known or understood.
                dispatcher.utter_message(text=f"Perdon, pero el documento '{doc}' no lo conozco.")
            elif niv_est is None or niv is None:
                #
                doc_name = DOCS[doc_idx]
                dispatcher.utter_message(
                    text=f"Conozco el {doc_name.title()}, ¿pero que parte quisieras?"
                )
            else:
                doc_id = DOC_IDS[doc_idx]
                # Index 3 contains the `text` field.
                res = db.retrieve_structural_division(doc_id, niv_est, int(niv))

                if res is None:
                    ftext = (
                        "No pude encontrar algun reglamento con la siguiente informacion &#129300; <br>"
                        f"<b>Documento</b>: {doc}, <b>{niv_est} {niv}</b>"
                    )
                else:
                    ftext = sd_html(format_title(res[2]), res[1].capitalize(), res[4], res[3])

                dispatcher.utter_message(text=ftext)

        return [FollowupAction("action_reset_slots")]


class ActionSimilaritySearch(Action):
    def name(self) -> Text:
        return "action_similarity_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        text = tracker.latest_message["text"]
        norm_text = nlputils.normalize_sentence(text)
        arts = self.__fetch_articles(text)

        if not arts:
            message_text = f"No se encontraron art&iacute;culos con los conceptos {norm_text}"
        else:
            results = []
            for a in arts:
                results.append(sd_html(format_title(a[0]), a[1].capitalize(), a[2], ""))

            ftext = "<br>".join(results)
            message_text = f"Busqueda realizada con conceptos <i>{norm_text}<i><br>{ftext}"

        dispatcher.utter_message(text=message_text)
        return []

    @classmethod
    def __fetch_articles(cls, text: str) -> List[str]:
        """Fetches similar articles using concepts from `text`."""
        _, sd_ids = nlputils.WordSpace.search(text)

        if not sd_ids:
            return []

        return db.retrieve_struct_div_by_word_id(
            sd_ids, fields="id_documento, id_nivel, numeracion, texto"
        )


class ResetSlots(Action):
    def name(self):
        return "action_reset_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [
            SlotSet("documento", None),
            SlotSet("nivel_estructural", None),
            SlotSet("nivel", None),
        ]
