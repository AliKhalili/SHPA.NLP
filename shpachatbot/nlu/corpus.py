import collections


class Corpus:
    def __init__(self):
        self._sentences = {}
        self._words = collections.defaultdict(int)
        self._last_sentence = 0

    def add_sentence(self, sentence: str):
        if sentence:
            self._sentences[self._last_sentence] = sentence
            for word in sentence.split(' '):
                self._words[word] += 1
            self._last_sentence += 1


if __name__ == "__main__":
    import os
    from shpachatbot.nlu.html_utils.parser import HmashahriParser

    corpus = Corpus()
    html_path_base = 'D:\\_temp\\crawler\\hamshahri'
    for file in os.listdir(html_path_base):
        hamshahri_html = HmashahriParser(os.path.join(html_path_base, file))
        fields = hamshahri_html.parse()
        for sentence in fields['post_content'].split('.'):
            corpus.add_sentence(sentence)

    print(corpus._words)
