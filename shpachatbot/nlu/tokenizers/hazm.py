from typing import Dict, Text, Any, List
from hazm import Normalizer, sent_tokenize, word_tokenize, Stemmer, Lemmatizer, POSTagger

from shpachatbot.nlu.components import Component
from shpachatbot.nlu.models import Message, Token, Sentence
from shpachatbot.constants import TOKEN_ATTRIBUTE_STEM, TOKEN_ATTRIBUTE_LEMM, TOKEN_ATTRIBUTE_POS


class HazmNormalizer(Component):
    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        super().__init__(component_config)
        self._normalizer = Normalizer()

    def process(self, message: Message, **kwargs: Any) -> None:
        message.text = self._normalizer.normalize(message.text)
        exclude_items = {}
        if 'exclude_items' in kwargs:
            exclude_items = {x: x for x in kwargs['exclude_items']}
        for key, value in message:
            if key in exclude_items:
                continue
            if isinstance(value, str):
                message[key] = self._normalizer.normalize(value)
            elif isinstance(value, list):
                for idx, item_value in enumerate(value):
                    value[idx] = self._normalizer.normalize(item_value)


class HazmTokenizer(Component):
    defaults = {"stemmer": True, "lemmatizer": True, 'pos': False}

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:

        super().__init__(component_config)
        if self.component_config.stemmer:
            self._stemmer = Stemmer()

        if self.component_config.lemmatizer:
            self._lemmatizer = Lemmatizer()

        if self.component_config.pos:
            self._pos_tagger = POSTagger(model='resources/postagger.model')

    def required_packages(self) -> List[Text]:
        return ['hazm']

    def process(self, message: Message, **kwargs: Any) -> None:
        text = message.text
        for sentence_str in sent_tokenize(text):
            sentence = Sentence(sentence_str)
            tokens = word_tokenize(sentence_str)
            pos_tags = []
            if self.component_config.pos:
                pos_tags = self._pos_tagger.tag(tokens)
            for idx, token_str in enumerate(tokens):
                token = Token(text=token_str)
                if self.component_config.stemmer:
                    token[TOKEN_ATTRIBUTE_STEM] = self._stemmer.stem(token_str)
                if self.component_config.lemmatizer:
                    token[TOKEN_ATTRIBUTE_LEMM] = self._lemmatizer.lemmatize(token_str)
                if self.component_config.pos:
                    token[TOKEN_ATTRIBUTE_POS] = pos_tags[idx][1]
                sentence.add_token(token)
            message.add_sentence(sentence)
