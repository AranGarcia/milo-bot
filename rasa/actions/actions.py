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
nlputils.WordSpace.load_clusters_from_file("docs/wv.npy")
nlputils.WordSpace.load_similarities_from_file("docs/sm.npy")
nlputils.WordSpace.load_binary_representations()


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
                res = db.retrieve_structural_division(doc_id, niv_est, int(niv))[3]
                dispatcher.utter_message(text=res)

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
        arts = self.__fetch_articles(text)

        # TODO: Format beautifully
        # Index 3 contains the text
        result = "\n".join(a[3] for a in arts)

        dispatcher.utter_message(text=result)
        return []

    @classmethod
    def __fetch_articles(cls, text, n_articles=3) -> List[str]:
        """Fetches similar articles using concepts from `text`."""
        # 1. Normalize text.
        concepts = nlputils.normalize_sentence(text)
        # 2. Create vector
        binary_vector = nlputils.WordSpace.bvectorize(concepts)
        # 3. Calculare similarities
        # FIXME: Indexes assumes that each row is a one-to-one match with an ID in `division_estructural`
        #        This may cause bugs as the rows can be switched (hope not).
        indexes = cls.__calculate_similarities(binary_vector, n_articles)
        # 4. Fetch most similar articles.
        return db.retrieve_struct_div_by_ids(
            sd_ids=tuple(indexes),
            fields="id, id_nivel, id_documento, texto, numeracion",
        )

    @staticmethod
    def __calculate_similarities(q, n_min):
        """Calculates similarities of a query vector `q` upon a collection of binary sentences."""
        # BS is the binary sentences of our collectio
        bs = nlputils.WordSpace.binary_vectors
        # W is the similarity matrix.
        W = nlputils.WordSpace.smatrix

        similarities = np.apply_along_axis(
            lambda s: (q.dot(W).dot(s)) / (np.linalg.norm(q) * np.linalg.norm(s)), axis=1, arr=bs
        )

        # Indexes should all be int type
        return [int(i) for i in similarities.argsort()[-3:] + 1]


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
