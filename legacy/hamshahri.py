import os
from concurrent import futures

import requests
from tqdm import tqdm

baseUrl = 'https://www.hamshahrionline.ir/news/{id}'
base_path = 'D:\_temp\crawler\hamshahri'
id_gent = range(577318, 1, -1)
default_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

download_pages = {int(f): f for f in os.listdir(base_path)}


def download_one(page_id):
    url = baseUrl.format(id=page_id)
    output_path = os.path.join(base_path, str(page_id))
    if page_id in download_pages:
        return True
    try:
        response = requests.get(url, headers=default_headers)
        if response.status_code == 200:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
    except Exception as error:
        return False


def download_all():
    max_workers = 8
    with futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(tqdm(executor.map(download_one, id_gent), total=len(id_gent)))
    return results


download_all()
