from typing import Dict, Text, Any, List
from hazm import Normalizer, sent_tokenize, word_tokenize, Stemmer, Lemmatizer, POSTagger

from shpachatbot.nlu.message import Message
from shpachatbot.nlu.tokenizers.tokenizer import Tokenizer, Token

SENTENCE, WORD, STEM, LEMM, TAG = "sentence", "word", "stem", "lemma", "tag"


class HazmTokenizer(Tokenizer):
    defaults = {"normalize": True, "stemmer": True, "lemmatizer": True}

    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        """Construct a new tokenizer using the WhitespaceTokenizer framework."""

        super().__init__(component_config)
        if self.component_config.normalize:
            self._normalizer = Normalizer()
        if self.component_config.stemmer:
            self._stemmer = Stemmer()
        if self.component_config.lemmatizer:
            self._lemmatizer = Lemmatizer()

    def required_packages(self) -> List[Text]:
        return ['hazm']

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        if self.component_config.normalize:
            text = self._normalizer.normalize(text)
        tokens = []

        sentence_number = 0
        for sent in sent_tokenize(text):
            sentence_number += 1
            words = word_tokenize(sent)
            for idx, word in enumerate(words):
                token = Token(text=word)
                token.set(SENTENCE, sentence_number)
                if self.component_config.stemmer:
                    token.set(STEM, self._stemmer.stem(word))
                if self.component_config.lemmatizer:
                    token.set(LEMM, self._lemmatizer.lemmatize(word))
                tokens.append(token)

        return tokens


if __name__ == "__main__":
    from shpachatbot.constants import TEXT

    hazm_tokenizer = HazmTokenizer.create(component_config={"stemmer": True})
    text = """
    به گزارش خبرنگار پایگاه خبری بانک مسکن-هیبنا،
    به تازگی و با راه اندازی حساب سپرده سرمایه گذاری آتیه طلایی 3 برای جذب سپرده ها
    و پس اندازها با محوریت طیف گسترده مشتریان،
    امکان تازه ای به منظور بسترسازی برای گسترش فرهنگ پس انداز به واسطه این امر فراهم شده است.
    """
    message = Message()
    message.set(TEXT, text, add_to_output=True)
    tokens = hazm_tokenizer.tokenize(message, TEXT)
    print(*tokens, sep='\n')
