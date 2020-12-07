from difflib import SequenceMatcher
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


DOCS = [
    "reglamento interno",
    "reglamento general de estudios",
    "reglamento de titulacion profesional",
    "ley organica",
]


def _str_sim(a, b):
    return SequenceMatcher(None, a=a, b=b).ratio()


def identify_document(doc):
    sims = [_str_sim(d) for d in DOCS]
    val, idx = min((val, idx) for (idx, val) in enumerate(sims))
    if val < 6.5:
        return -1

    return DOCS[idx]


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

        # TODO: Determine response the search level given the possible combinations of entities.

        if doc is None:
            response_text = "¿De qué documento?"
        else:
            response_text = (
                f"Document: {doc}, {tracker.latest_message['entities']}---{domain}"
            )

        dispatcher.utter_message(text=response_text)
        return []


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
