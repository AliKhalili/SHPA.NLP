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

    def __contains__(self, attr_key):
        if attr_key in self._attrs:
            return True
        return False

    def __getitem__(self, attr_key):
        if attr_key in self:
            return self._attrs[attr_key]
        return None


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

    def add_field(self, *, field_name: str, css_selector: str, is_multi: bool = False, value_from=None):
        self._fields[field_name] = HtmlField(name=field_name,
                                             selector=css_selector,
                                             is_multi=is_multi,
                                             value_from=value_from)

    def parse(self):
        result = {}
        for field in self:
            result[field.name] = self._parse_field(field.name)
        return result

    def _parse_field(self, field_name):
        field = self[field_name]
        selected = []
        if 'is_multi' in field and field['is_multi']:
            selected = [e for e in self._soup.select(field.selector)]
        else:
            selected.append(self._soup.select_one(self[field_name].selector))

        if 'value_from' in field and field['value_from']:
            selected = [s[field['value_from']] for s in selected if s.has_attr(field['value_from'])]
        else:
            selected = [s.text for s in selected]

        if len(selected) == 1:
            return selected[0]
        else:
            return selected


class HmashahriParser(HtmlParser):
    def __init__(self, html_path: str):
        super(HmashahriParser, self).__init__(html_path)
        super().add_field(field_name='post_title', css_selector='h1.title > a')
        # super().add_field(field_name='post_subtitle', css_selector='div.newstitle > h4.rutitr')
        super().add_field(field_name='post_content', css_selector='div.item-text')


class Way2PayParser(HtmlParser):
    def __init__(self, html_path: str):
        super(Way2PayParser, self).__init__(html_path)
        super().add_field(field_name='post_badges', css_selector='div.post-header-title span.term-badge', is_multi=True)
        super().add_field(field_name='post_title', css_selector='h1.single-post-title')
        super().add_field(field_name='post_tags', css_selector='.post-tags a', is_multi=True)
        # super().add_field(field_name='post_content', css_selector='.entry-content')
        super().add_field(field_name='post_date', css_selector='time.post-published', value_from='datetime')


if __name__ == "__main__":
    # html_path_base = 'D:\\_temp\\crawler\\hamshahri'
    # for file in os.listdir(html_path_base):
    #     hamshahri_html = HmashahriParser(os.path.join(html_path_base, file))
    #     fields = hamshahri_html.parse()
    #     print(fields)

    html_path_base = 'D:\\_temp\\crawler\\way2pay\\posts'
    for file in os.listdir(html_path_base):
        html_parser = Way2PayParser(os.path.join(html_path_base, file))
        fields = html_parser.parse()
        fields['id'] = file
        print(fields)
