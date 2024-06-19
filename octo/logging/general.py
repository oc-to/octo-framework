import logging
import logging.config
from octo.logging.config import OCTO_LOGGING


class Logger:
    def __init__(self) -> None:
        self._config = OCTO_LOGGING
        self._loging_name = "octo-log"

    def get(self) -> logging:
        logging.config.dictConfig(self._config)
        return logging.getLogger(self._loging_name)
