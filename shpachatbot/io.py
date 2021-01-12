import json
import os
from pathlib import Path
from typing import Union, Text, Dict, Any, List

from ruamel import yaml as yaml
from elasticsearch import Elasticsearch
from yaml import YAMLError

from shpachatbot.exceptions import YamlSyntaxException

DEFAULT_ENCODING = "utf-8"
YAML_VERSION = (1, 2)


def read_file(filename: Union[Text, Path], encoding: Text = DEFAULT_ENCODING) -> Any:
    """Read text from a file."""

    with open(filename, encoding=encoding) as f:
        return f.read()


def fix_yaml_loader() -> None:
    """Ensure that any string read by yaml is represented as unicode."""

    def construct_yaml_str(self, node):
        # Override the default string handling function
        # to always return unicode objects
        return self.construct_scalar(node)

    yaml.Loader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)
    yaml.SafeLoader.add_constructor("tag:yaml.org,2002:str", construct_yaml_str)


def _is_ascii(text: Text) -> bool:
    return all(ord(character) < 128 for character in text)


def read_yaml(content: Text, reader_type: Union[Text, List[Text]] = "safe") -> Any:
    """Parses yaml from a text.

    Args:
        content: A text containing yaml content.
        reader_type: Reader type to use. By default "safe" will be used

    Raises:
        ruamel.yaml.parser.ParserError: If there was an error when parsing the YAML.
    """
    fix_yaml_loader()

    yaml_parser = yaml.YAML(typ=reader_type)
    yaml_parser.version = YAML_VERSION
    yaml_parser.preserve_quotes = True
    yaml.allow_duplicate_keys = False

    if _is_ascii(content):
        # Required to make sure emojis are correctly parsed
        content = (
            content.encode("utf-8")
                .decode("raw_unicode_escape")
                .encode("utf-16", "surrogatepass")
                .decode("utf-16")
        )

    return yaml_parser.load(content) or {}


def read_yaml_file(filename: Union[Text, Path]) -> Union[List[Any], Dict[Text, Any]]:
    """Parses a yaml file.

    Raises an exception if the content of the file can not be parsed as YAML.

    Args:
        filename: The path to the file which should be read.

    Returns:
        Parsed content of the file.
    """
    try:
        return read_yaml(read_file(filename, DEFAULT_ENCODING))
    except YAMLError as e:
        raise YamlSyntaxException(filename, e)


def read_config_file(filename: Union[Path, Text]) -> Dict[Text, Any]:
    """Parses a yaml configuration file. Content needs to be a dictionary

    Args:
        filename: The path to the file which should be read.
    """
    content = read_yaml_file(filename)

    if content is None:
        return {}
    elif isinstance(content, dict):
        return content
    else:
        raise YamlSyntaxException(
            filename,
            ValueError(
                f"Tried to load configuration file '{filename}'. "
                f"Expected a key value mapping but found a {type(content).__name__}"
            ),
        )


def json_to_string(obj: Any, **kwargs: Any) -> Text:
    """Dumps a JSON-serializable object to string.

    Args:
        obj: JSON-serializable object.
        kwargs: serialization options. Defaults to 2 space indentation
                and disable escaping of non-ASCII characters.

    Returns:
        The objects serialized to JSON, as a string.
    """
    indent = kwargs.pop("indent", 2)
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, indent=indent, ensure_ascii=ensure_ascii, **kwargs)


class ElasticStore:
    def __init__(self, index="posts"):
        self._index = index
        self._es = Elasticsearch()

    def dump_json(self, doc):
        res = self._es.index(index=self._index, body=doc)
        # The result of the indexing operation, created or updated.
        return res['result']
