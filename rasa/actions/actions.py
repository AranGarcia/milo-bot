from difflib import SequenceMatcher
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.executor import CollectingDispatcher

from lib.db import retrieve_structural_division


DOCS = [
    "reglamento interno",
    "reglamento general de estudios",
    "reglamento de titulacion profesional",
    "ley organica",
]


def _str_sim(a, b):
    return SequenceMatcher(None, a, b).ratio()


def identify_document(doc_name):
    sims = [_str_sim(doc_name.lower(), d) for d in DOCS]
    val, idx = max((val, idx) for (idx, val) in enumerate(sims))
    if val < 0.65:
        return -1
    return idx


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

        response_text = self.__generate_message(doc, niv_est, niv)

        dispatcher.utter_message(text=response_text)
        return [FollowupAction("action_reset_slots")]

    @staticmethod
    def __generate_message(doc, niv_est, niv):
        # First determine the document
        if doc is None:
            return "¿De qué documento necesitas extraer informacion?"

        doc_idx = identify_document(doc)
        if doc_idx < 0:
            return f'Perdon, pero el documento "{doc}" no lo conozco.'

        doc_name = DOCS[doc_idx]

        if niv_est is None or niv is None:
            return f"Conozco el {doc_name.title()}, ¿pero que parte quisieras?"

        return f"DOCUMENTO: {doc_name.title()}, NIVEL: {niv_est.capitalize()}, ENUMERACION: {niv}"


class ActionSimilaritySearch(Action):
    def name(self) -> Text:
        return "action_similarity_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="¿Quieres realizar una consulta? Espera, que no tengo los documentos. :("
        )
        return []


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
