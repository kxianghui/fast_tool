# -*- coding: utf-8 -*-
__author__ = 'hkhl'

import json
from typing import Set, Any


class JsonExtractor:
    @staticmethod
    def extract_values(json_text: str, key_path: str) -> Set[Any]:
        """
        Extract values from JSON text using dot notation path
        :param json_text: JSON string to parse
        :param key_path: Dot separated path to extract (e.g. "data.result.name")
        :return: Set of extracted values
        """
        try:
            json_data = json.loads(json_text)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

        keys = key_path.split('.')
        result = list()
        JsonExtractor._extract_recursive(json_data, keys, 0, result)
        return result

    @staticmethod
    def _extract_recursive(data: Any, keys: list, index: int, result: list) -> None:
        """
        Recursively traverse JSON structure to extract values
        """
        if index >= len(keys):
            result.append(data)
            return

        current_key = keys[index]

        if isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    JsonExtractor._extract_recursive(item, keys, index, result)
        elif isinstance(data, dict):
            if current_key in data:
                JsonExtractor._extract_recursive(data[current_key], keys, index + 1, result)
            else:
                raise KeyError(f"Key '{current_key}' not found in JSON structure")
        else:
            raise ValueError(f"Cannot traverse through non-container value: {data}")