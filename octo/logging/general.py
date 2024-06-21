import logging
import logging.config
from octo.logging.config import OCTO_LOGGING, OCTO_LOGGER_NAME


class Logger:
    def __init__(self) -> None:
        self._config = OCTO_LOGGING
        self._loging_name = OCTO_LOGGER_NAME

    def get(self) -> logging:
        logging.config.dictConfig(self._config)
        return logging.getLogger(self._loging_name)
