import os
from typing import Optional
from bs4 import BeautifulSoup

from shpachatbot.exceptions import SHPAException


class HtmlFileNotFoundException(SHPAException):
    def __init__(self, filename: Optional[str] = None) -> None:
        self.filename = filename

    def __str__(self) -> str:
        if self.filename:
            exception_text = f"Failed to read '{self.filename}'"
        else:
            exception_text = "Failed to read html_utils file"

        return exception_text


class HtmlFieldNotFoundException(SHPAException):
    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    def __str__(self) -> str:
        exception_text = ""
        if self.field_name:
            exception_text = f"Failed to read '{self.field_name}', at first you should add this field to the parser"
        return exception_text


def get_filename_from_abspath(abs_path: str) -> str:
    return os.path.splitext(abs_path)[0]


def get_file_content(html_path: str):
    if not os.path.exists(html_path):
        raise HtmlFileNotFoundException(filename=get_filename_from_abspath(html_path))

    with open(html_path, 'r', encoding='utf-8') as read_file:
        return read_file.read()


class HtmlField:
    def __init__(self, *, name, selector, **attrs):
        self._name = name
        self._selector = selector
        self._attrs = attrs

    @property
    def name(self):
        return self._name

    @property
    def selector(self):
        return self._selector


class HtmlParser:
    def __init__(self, html_path: str):
        self._html_content = get_file_content(html_path)
        self._soup = BeautifulSoup(self._html_content, "lxml")
        self._fields = {}

    def __getitem__(self, field_name):
        try:
            return self._fields[field_name]
        except KeyError:
            raise HtmlFieldNotFoundException(field_name=field_name)

    def __iter__(self):
        for field_name, field in self._fields.items():
            yield field

    def add_field(self, *, field_name: str, css_selector: str, is_multi: bool = False):
        self._fields[field_name] = HtmlField(name=field_name, selector=css_selector, is_multi=is_multi)

    def parse(self):
        result = {}
        for field in self:
            result[field.name] = self._parse_field(field.name)
        return result

    def _parse_field(self, field_name):
        text = self._soup.select_one(self[field_name].selector).text
        return text


class HmashahriParser(HtmlParser):
    def __init__(self, html_path: str):
        super(HmashahriParser, self).__init__(html_path)
        super().add_field(field_name='post_title', css_selector='h1.title > a')
        # super().add_field(field_name='post_subtitle', css_selector='div.newstitle > h4.rutitr')
        super().add_field(field_name='post_content', css_selector='div.item-text')


if __name__ == "__main__":
    html_path_base = 'D:\\_temp\\crawler\\hamshahri'
    for file in os.listdir(html_path_base):
        hamshahri_html = HmashahriParser(os.path.join(html_path_base, file))
        fields = hamshahri_html.parse()
        print(fields)
