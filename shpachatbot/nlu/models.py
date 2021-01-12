import json
from typing import Text, Optional, Dict, Any, List


def to_json(dic: Dict) -> Text:
    return json.dumps(dic, indent=4, ensure_ascii=False)


class Token:
    def __init__(
            self,
            text: Text,
            properties: Optional[Dict[Text, Any]] = None,
    ) -> None:
        self.text = text
        self._properties = properties if properties else {}
        self._exclude_properties = []

    @property
    def dict(self) -> Dict:
        json_dict = {"text": self.text}
        for key, value in self._properties.items():
            json_dict[key] = value
        return json_dict

    def __setitem__(self, key: Text, value: Any) -> None:
        self._properties[key] = value

    def __getitem__(self, key: Text) -> Any:
        return self._properties.get(key)

    def __repr__(self):
        props = []
        if self._properties:
            props = [f"{key}:'{value}'" for key, value in self._properties.items()
                     if key not in self._exclude_properties]
        return f"<Token text: '{self.text}'{' ,'.join(props)}>"


class Sentence:
    def __init__(
            self,
            text: Text,
            tokens: Optional[List[Token]] = None,
            properties: Optional[Dict[Text, Any]] = None
    ) -> None:
        self.text = text
        self._tokens = tokens if tokens else []
        self._properties = properties if properties else {}

    def __setitem__(self, key: Text, value: Any) -> None:
        self._properties[key] = value

    def __getitem__(self, key: Text) -> Any:
        return self._properties.get(key)

    def add_token(self, token: Token) -> None:
        self._tokens.append(token)

    @property
    def tokens(self):
        return self._tokens

    @property
    def dict(self) -> Dict:
        json_dict = {
            'text': self.text,
            'tokens_count': len(self._tokens),
            'tokens': [t.dict for t in self._tokens]
        }
        for key, value in self._properties.items():
            json_dict[key] = value
        return json_dict


class Message:
    def __init__(
            self,
            text: Text,
            sentences: Optional[List[Sentence]] = None,
            properties: Optional[Dict[Text, Any]] = None,
    ) -> None:
        self.text = text
        self._sentences = sentences if sentences else []
        self._properties = properties if properties else {}

    def add_sentence(self, sentence: Sentence) -> None:
        self._sentences.append(sentence)

    def __setitem__(self, key: Text, value: Any) -> None:
        self._properties[key] = value

    def __getitem__(self, key: Text) -> Any:
        return self._properties.get(key)

    def __iter__(self):
        for key, value in self._properties.items():
            yield key, value

    @property
    def sentences(self):
        return self._sentences

    @property
    def json(self) -> Text:
        json_dict = {
            'text': self.text,
            'sentences_count': len(self._sentences),
        }
        for key, value in self._properties.items():
            json_dict[key] = value
        if self._sentences:
            json_dict['sentences'] = [s.dict for s in self._sentences]
        return to_json(json_dict)
