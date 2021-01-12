from typing import Dict, Text, Any, List
from nltk import ngrams

from shpachatbot.nlu.components import Component
from shpachatbot.nlu.models import Message
from shpachatbot.nlu.tokenizers.hazm import HazmTokenizer


class Ngrams(Component):
    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """Construct a new tokenizer using the WhitespaceTokenizer framework."""

        super().__init__(component_config)

    def required_packages(self) -> List[Text]:
        return ['nltk']

    def process(self, message: Message, **kwargs: Any) -> None:
        n = 2
        if 'n' in kwargs:
            n = kwargs['n']
        for sentence in message.sentences:
            tokens = [t.text for t in sentence.tokens]
            if n <= len(tokens):
                t = [' '.join(g) for g in ngrams(tokens, n)]
                sentence[f"{n}grams"] = [' '.join(g) for g in ngrams(tokens, n)]
