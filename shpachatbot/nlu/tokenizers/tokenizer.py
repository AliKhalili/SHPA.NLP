from abc import abstractmethod
from typing import Text, Any, Dict, List, Optional

from shpachatbot.constants import MESSAGE_ATTRIBUTES, TOKENS_NAMES
from shpachatbot.nlu.components import Component
from shpachatbot.nlu.message import Message


class Token:
    def __init__(
            self,
            text: Text,
            data: Optional[Dict[Text, Any]] = None,
    ) -> None:
        self.text = text
        self.data = data if data else {}

    def set(self, prop: Text, info: Any) -> None:
        self.data[prop] = info

    def get(self, prop: Text, default: Optional[Any] = None) -> Any:
        return self.data.get(prop, default)

    def __repr__(self):
        props = []
        if self.data:
            props = [f"{key}:'{value}'" for key, value in self.data.items()]
        return f"<Token text: '{self.text}'{' ,'.join(props)}>"


class Tokenizer(Component):
    def __init__(self, component_config: Dict[Text, Any] = None) -> None:

        super().__init__(component_config)

    def process(self, message: Message, **kwargs: Any) -> None:
        for attribute in MESSAGE_ATTRIBUTES:
            if isinstance(message.get(attribute), str):
                tokens = self.tokenize(message, attribute)
                message.set(TOKENS_NAMES[attribute], tokens)

    @abstractmethod
    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        raise NotImplementedError
