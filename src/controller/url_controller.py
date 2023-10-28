import json
from typing import Any

from aws_lambda_powertools import Logger

from src.services.config import ConfigService


class UrlController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_url_shorten(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        return {"message": "OK"}

    def retrieve_url_shorten(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = json.loads(self.event.get("body", {}))

        return {"message": "OK"}
