# Module for parsing Legal documents
import json
import yaml

from .items import ItemType, LegalDocItem


class LegalFileStructure:
    def __init__(self):
        self.content = {}

        # State variables
        self._last_item = None
        self._current_item = None
        self._stack = []

    def write_file(self, fname, file_format) -> str:
        if file_format == "yaml":
            fname = f"{fname}.yaml"
            with open(fname, "w", encoding="utf-8") as f:
                yaml.dump(
                    self.content,
                    stream=f,
                    encoding="utf-8",
                    allow_unicode=True
                )
        elif file_format == "json":
            fname = f"{fname}.json"
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(self.content, f, ensure_ascii=False)
        else:
            raise ValueError(f"Unrecognized format {file_format}.")

        return fname

    def add_item(self, item: LegalDocItem) -> None:
        # if not isinstance(item, LegalDocItem):
        #     raise ValueError(f"invalid type {item}, expected {LegalDocItem}")

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
        for i in range(len(self._stack) - 1):
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
