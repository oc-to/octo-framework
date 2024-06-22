import logging
import logging.config
from octo.logging.config import OCTO_LOGGING, OCTO_LOGGER_NAME
import re


class Logger:
    def __init__(self) -> None:
        self._config = OCTO_LOGGING
        self._loging_name = OCTO_LOGGER_NAME

    def get(self) -> logging:
        logging.config.dictConfig(self._config)
        return logging.getLogger(self._loging_name)

    def sanitize_message(self, message: str) -> str:
        """Sanitize the message by removing newlines, tabs,
        and replacing them with spaces."""
        return re.sub(r"[\n\r\t]", " ", message)
