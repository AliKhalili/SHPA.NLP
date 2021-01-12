import os
from typing import Text, TypeVar, Type

from shpachatbot.nlu.html_utils.parser import Way2PayParser, HtmlParser
from shpachatbot.nlu.tokenizers.hazm import HazmTokenizer, HazmNormalizer
from shpachatbot.nlu.train.ngrams import Ngrams
from shpachatbot.worker import worker_start

config_path = "D:\\ProjectServer\\SHPA.NLP\\shpachatbot\\config\\default_config.yml"

TParser = TypeVar("TParser", bound=HtmlParser)


class PreProcessor:
    def __init__(self, html_file_full_path: Text, out_path: Text) -> None:
        if not os.path.exists(html_file_full_path):
            raise FileNotFoundError

        self._out_path = out_path
        self._input_path = html_file_full_path
        self._normalizer = HazmNormalizer.create()
        self._tokenizer = HazmTokenizer.create(component_config={"stemmer": True})
        self._ngram = Ngrams()
        self._parser_cls = None

    def _single_process(self, file_name: Text):
        file_path = os.path.join(self._input_path, file_name)
        if os.path.isdir(file_path):
            return
        parser = self._parser_cls(file_path)
        messages = parser.parse_to_messages()
        for m_item in messages:
            self._normalizer.process(m_item, exclude_items=['id', 'post_date'])

            self._tokenizer.process(m_item)
            # self._ngram.process(m_item, n=2)
            # self._ngram.process(m_item, n=3)
            # self._ngram.process(m_item, n=4)
            # self._ngram.process(m_item, n=5)
            # self._ngram.process(m_item, n=6)

            path = os.path.join(self._out_path, f"{m_item['id'].strip().replace(' ', '_').replace('.', '_')}.json")
            if os.path.exists(path):
                os.remove(path)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(m_item.json)

    def process(self, parser_cls: Type[TParser]):
        self._parser_cls = parser_cls
        worker_start(worker_func=self._single_process,
                     worker_itr=os.listdir(self._input_path),
                     workers=4,
                     enable_tqdm=True)


if __name__ == "__main__":
    html_file_full_path = "D:/_temp/crawler/way2pay/posts"
    # html_file_full_path = "D:/_temp/crawler/melli_fqq/post"
    out_path = "D:/_temp/crawler/pre_process"

    preprocessor = PreProcessor(html_file_full_path=html_file_full_path, out_path=out_path)
    preprocessor.process(Way2PayParser)
    # preprocessor.process(MelliFaqParser)
