from typing import Optional, Dict, Text, Any, Set, List

from shpachatbot.constants import TEXT


class Message:
    def __init__(
            self,
            data: Optional[Dict[Text, Any]] = None,
            output_properties: Optional[Set] = None,
            time: Optional[Text] = None,
            features: Optional[List["Features"]] = None,
            **kwargs: Any,
    ) -> None:
        self.time = time
        self.data = data.copy() if data else {}
        self.features = features if features else []
        self.output_properties = output_properties if output_properties else set()

        self.data.update(**kwargs)

        self.output_properties.add(TEXT)

    def set(self, prop, info, add_to_output=False) -> None:
        self.data[prop] = info
        if add_to_output:
            self.output_properties.add(prop)

    def get(self, prop, default=None) -> Any:
        return self.data.get(prop, default)