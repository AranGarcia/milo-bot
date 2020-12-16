# Module for parsing Legal documents
import os

import json

from .base import ItemType, LegalDocItem


class LegalFileStructure:
    def __init__(self):
        self.content = {}

        # State variables
        self._last_item = None
        self._current_item = None
        self._stack = []

    def write_file(self, fname, dest_dir="./json/") -> str:
        fname = os.path.basename(fname)
        fpath = f"{os.path.realpath(dest_dir)}/{fname}.json"
        print('\twriting to', fpath)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(self.content, f, ensure_ascii=False)

        return fname

    def add_item(self, item: LegalDocItem) -> None:
        if not isinstance(item, LegalDocItem):
            raise ValueError(f"invalid type {item}, expected {LegalDocItem}")

        self._last_item = self._current_item
        self._current_item = item
        if self._last_item is None:
            if self._current_item is not None:
                # Initial state
                self._stack.append(item.itemtype)
                self.content["level"] = item.itemtype.name
                self.content["items"] = [
                    {"text": item.text, "enum": item.enumeration, "content": {}}
                ]
            return
        else:
            self._calculate_state()
            self._update()

    def _calculate_state(self):
        # State machine
        last_item = self._last_item.itemtype
        current_item = self._current_item.itemtype

        if last_item.value < current_item.value:
            # Current item is a child of last item
            self._stack.append(current_item)
        elif last_item.value > current_item.value:
            # Find a node in the same level
            while self._stack[-1].value > current_item.value:
                self._stack.pop()

    def _update(self):
        item_list = self.content["items"]
        for _ in range(len(self._stack) - 1):
            content = item_list[-1]["content"]
            if not content:
                # An item will be expanded
                content["level"] = self._current_item.itemtype.name
                content["items"] = []

            item_list = content["items"]

        item_dict = {
            "text": self._current_item.text.lower(),
            "enum": self._current_item.enumeration,
        }
        # Articles have no content
        if self._current_item.itemtype != ItemType.ARTICULO:
            item_dict["content"] = {}

        item_list.append(item_dict)
