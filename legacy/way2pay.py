import os
import re

from bs4 import BeautifulSoup


def find_all_post_links(archive_path):
    post_pattern = re.compile("https://way2pay.ir/([0-9]+)/")
    find_urls = set()
    for archive_file in os.listdir(archive_path):
        with open(os.path.join(archive_path, archive_file), 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), "lxml")
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                if post_pattern.match(href):
                    match = post_pattern.match(href)
                    find_urls.add(match[0])
    return list(find_urls)


urls = find_all_post_links("D:\\_temp\\crawler\\way2pay\\archive")
print(len(urls))
with open("D:\\_temp\\crawler\\way2pay\\urls.txt", 'w', encoding='utf-8') as fp:
    fp.writelines('\n'.join(urls))
