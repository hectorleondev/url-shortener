import json
from typing import Any

from aws_lambda_powertools import Logger

from src.data.data_type import URLRequest
from src.data.exceptions import BadRequestException
from src.services.config import ConfigService
from src.services.db import get_url_by_path, save_url, get_url
from src.services.util import to_base62, generate_id, to_base10
from src.services.validation import validate_event


class UrlController:
    def __init__(self, _conf_svc: ConfigService, _event: Any, _logger: Logger):
        self.conf_svc = _conf_svc
        self.logger = _logger
        self.event = _event

    def create_shortcode(self):
        """
        Save new record in table and create new shortcode
        :return:
        """
        self.logger.info({"message": "Event information", "event_info": self.event})

        body = {} if not self.event.get("body") else json.loads(self.event.get("body"))

        validate_event(body, "create_url_shorten")

        data = URLRequest.from_dict(body)

        url_data = get_url_by_path(data.url)

        if not url_data:
            url_id = generate_id()
            save_url(url_id, data.url, data.title)
        else:
            url_id = url_data[0].url_id
        response = {
            "shortcode": to_base62(url_id),
        }
        return response

    def retrieve_url_data(self):
        """
        Retrieve url data from shortcode
        :return:
        """
        self.logger.info({"message": "Event information", "event_info": self.event})

        validate_event(self.event, "retrieve_url_shorten")

        shortcode = self.event.get("queryStringParameters").get("shortcode")

        url_id = to_base10(shortcode)

        url_data = get_url(url_id)
        if not url_data:
            raise BadRequestException("The shortcode is invalid")

        return {
            "url": url_data.url_path,
            "title": url_data.url_title,
            "created_at": url_data.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
