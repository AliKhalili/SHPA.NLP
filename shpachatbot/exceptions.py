from typing import Optional, Text


class SHPAException(Exception):
    """Base exception class for all errors raised by shpa chat bot."""


class YamlSyntaxException(SHPAException):
    """Raised when a YAML file can not be parsed properly due to a syntax error."""

    def __init__(
            self,
            filename: Optional[Text] = None,
            underlying_yaml_exception: Optional[Exception] = None,
    ) -> None:
        super(YamlSyntaxException, self).__init__(filename)

        self.underlying_yaml_exception = underlying_yaml_exception

    def __str__(self) -> Text:
        if self.filename:
            exception_text = f"Failed to read '{self.filename}'."
        else:
            exception_text = "Failed to read YAML."

        if self.underlying_yaml_exception:
            self.underlying_yaml_exception.warn = None
            self.underlying_yaml_exception.note = None
            exception_text += f" {self.underlying_yaml_exception}"

        if self.filename:
            exception_text = exception_text.replace(
                'in "<unicode string>"', f'in "{self.filename}"'
            )

        exception_text += (
            "\n\nYou can use https://yamlchecker.com/ to validate the "
            "YAML syntax of your file."
        )
        return exception_text
