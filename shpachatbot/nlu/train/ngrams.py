from typing import Dict, Text, Any, List
from nltk import ngrams

from shpachatbot.constants import TOKENS_NAMES, TEXT
from shpachatbot.nlu.components import Component
from shpachatbot.nlu.message import Message
from shpachatbot.nlu.tokenizers.hazm_tokenizer import HazmTokenizer


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
        tokens = [t.text for t in message.get(TOKENS_NAMES[TEXT])]
        message.set(f"{n}grams", [g for g in ngrams(tokens, n)])


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
    message.set(TOKENS_NAMES[TEXT], tokens)
    print(*tokens, sep='\n')
    ngram = Ngrams()
    ngram.process(message)
    ngram.process(message, n=3)
    ngram.process(message, n=4)
    for t in message.get("2grams"):
        print(t)
    for t in message.get("3grams"):
        print(t)
    for t in message.get("4grams"):
        print(t)
