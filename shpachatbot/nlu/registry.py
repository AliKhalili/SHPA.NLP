import importlib
import logging
from typing import Text, Type, Optional, Any, Dict

from shpachatbot.nlu.tokenizers.hazm_tokenizer import HazmTokenizer

logger = logging.getLogger(__name__)

component_classes = [
    HazmTokenizer
]
registered_components = {c.name: c for c in component_classes}


def class_from_module_path(
        module_path: Text, lookup_path: Optional[Text] = None
) -> Any:
    module_name, _, class_name = module_path.rpartition(".")
    m = importlib.import_module(module_name)
    return getattr(m, class_name)


def get_component_class(component_name: Text) -> Type["Component"]:
    if component_name not in registered_components:
        try:
            return class_from_module_path(component_name)

        except (ImportError, AttributeError) as e:
            print('TODO')
    return registered_components[component_name]


def create_component_by_config(
        component_config: Dict[Text, Any], config: "RasaNLUModelConfig"
) -> Optional["Component"]:
    component_name = component_config.get("class", component_config["name"])
    component_class = get_component_class(component_name)
    return component_class.create(component_config, config)
