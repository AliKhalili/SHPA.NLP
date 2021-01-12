import logging
from abc import abstractmethod
from typing import List, Type, Optional, Dict, Any, Text, Tuple

from pyrsistent import typing

from shpachatbot.config import NLUModelConfig
from shpachatbot.nlu.models import Message
from shpachatbot.utils import override_defaults

logger = logging.getLogger(__name__)


class Component:
    @property
    def name(self) -> Text:
        """Access the class's property name from an instance."""

        return type(self).__name__

    @classmethod
    def required_components(cls) -> List[Type["Component"]]:
        """Specify which components need to be present in the pipeline.

        Returns:
            The list of class names of required components.
        """

        return []

    defaults = {}

    def __init__(self, component_config: Optional[Dict[Text, Any]] = None) -> None:
        if not component_config:
            component_config = {}

        component_config["name"] = self.name

        self.component_config = override_defaults(
            self.defaults, component_config
        )

        self.component_config = NLUModelConfig(self.component_config)

    @classmethod
    def required_packages(cls) -> List[Text]:
        return []

    @classmethod
    def create(
            cls, component_config: Optional[Dict[Text, Any]] = None
    ) -> "Component":
        return cls(component_config)

    @abstractmethod
    def process(self, message: Message, **kwargs: Any) -> None:
        raise NotImplementedError
