import logging

from shpachatbot.nlu.tokenizers.hazm import HazmTokenizer

logger = logging.getLogger(__name__)

component_classes = [
    HazmTokenizer
]
registered_components = {c.name: c for c in component_classes}
