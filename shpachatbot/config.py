import logging
import os
from typing import Any, Dict, List, Optional, Text, Union

from shpachatbot.io import json_to_string

logger = logging.getLogger(__name__)


class NLUModelConfig:
    """A class that stores NLU model configuration parameters."""

    def __init__(self, configuration_values: Optional[Dict[Text, Any]] = None) -> None:
        """Create a model configuration.

        Args:
            configuration_values: optional dictionary to override defaults.
        """
        if not configuration_values:
            configuration_values = {}

        self.language = "en"
        self.pipeline = []
        self.data = None

        self.override(configuration_values)

        for key, value in self.items():
            setattr(self, key, value)

    def __getitem__(self, key: Text) -> Any:
        return self.__dict__[key]

    def get(self, key: Text, default: Any = None) -> Any:
        return self.__dict__.get(key, default)

    def __setitem__(self, key: Text, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: Text) -> None:
        del self.__dict__[key]

    def __contains__(self, key: Text) -> bool:
        return key in self.__dict__

    def __len__(self) -> int:
        return len(self.__dict__)

    def __getstate__(self) -> Dict[Text, Any]:
        return self.as_dict()

    def __setstate__(self, state: Dict[Text, Any]) -> None:
        self.override(state)

    def items(self) -> List[Any]:
        return list(self.__dict__.items())

    def as_dict(self) -> Dict[Text, Any]:
        return dict(list(self.items()))

    def view(self) -> Text:
        return json_to_string(self.__dict__, indent=4)

    @property
    def component_names(self) -> List[Text]:
        if self.pipeline:
            return [c.get("name") for c in self.pipeline]
        else:
            return []

    def override(self, config) -> None:
        if config:
            self.__dict__.update(config)
