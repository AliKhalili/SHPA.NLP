import datetime
import os
from concurrent import futures

import requests
from tqdm import tqdm


class Crawler:
    def __init__(self, base_url, idx_gen, output_path):
        self._base_url = base_url
        self._default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
        }
        self._idx_gen = idx_gen
        self._output_path = output_path
        self._download_pages = {f: f for f in os.listdir(output_path)}

    def _download_single(self, page_id):
        message = "{page_id}: {status_code}"
        # print(page_id)
        url = self._base_url.format(page_id=page_id)
        output_path = os.path.join(self._output_path, str(page_id.replace('/', '-')))
        if page_id in self._download_pages:
            return True
        try:
            response = requests.get(url, headers=self._default_headers)
            if response.status_code == 200:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(response.text)
        except Exception as error:
            pass

        print(message.format(page_id=url, status_code=response.status_code))

    def _download_all(self, workers=8):
        with futures.ThreadPoolExecutor(max_workers=workers) as executor:
            # results = list(tqdm(executor.map(self._download_single, self._idx_gen), total=len(self._idx_gen)))
            results = list(executor.map(self._download_single, self._idx_gen))
        return results

    def start(self, workers=8):
        self._download_all(workers)


if __name__ == "__main__":
    # base = datetime.datetime(2016, 10, 20)
    # date_list = [f"{(base - datetime.timedelta(days=x)):%Y/%m/%d}" for x in range(365 * 10)]
    # crwaler = Crawler(base_url='https://way2pay.ir/date/{page_id}',
    #                   idx_gen=date_list,
    #                   output_path="D:\\_temp\\crawler\\way2pay\\archive")
    # crwaler.start(workers=32)

    links = []
    with open("D:\\_temp\\crawler\\way2pay\\urls.txt", 'r', encoding='utf-8') as f:
        links = [link.strip()[:-1].split('/')[-1] for link in f.readlines()]

    crwaler = Crawler(base_url='https://way2pay.ir/{page_id}/',
                      idx_gen=links,
                      output_path="D:\\_temp\\crawler\\way2pay\\posts")
    crwaler.start(workers=32)
