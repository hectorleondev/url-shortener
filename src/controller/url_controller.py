import json
from typing import Any

from aws_lambda_powertools import Logger

from src.services.config import ConfigService
from src.services.validation import validate_event


class UrlController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_url_shorten(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = {} if not self.event.get("body") else json.loads(self.event.get("body"))

        validate_event(body, "create_url_shorten")

        return {"message": body}

    def retrieve_url_shorten(self):
        self.logger.info({"message": "Event information", "event_info": self.event})

        validate_event(self.event, "retrieve_url_shorten")

        return {"message": self.event["queryStringParameters"]}
