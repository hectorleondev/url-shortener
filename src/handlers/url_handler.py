from http import HTTPStatus

from aws_lambda_powertools import Logger

from src.controller.url_controller import UrlController
from src.services.config import ConfigService
from src.services.response import ResponseService


@ResponseService.pretty_response
def create_url_shorten_handler(event, context, conf_svc: ConfigService, logger: Logger):
    url_controller = UrlController(_conf_svc=conf_svc, _event=event, _logger=logger)
    response = url_controller.create_url_shorten()
    return HTTPStatus.CREATED, response


@ResponseService.pretty_response
def retrieve_url_shorten_handler(event, context, conf_svc: ConfigService, logger: Logger):
    url_controller = UrlController(_conf_svc=conf_svc, _event=event, _logger=logger)
    response = url_controller.retrieve_url_shorten()
    return HTTPStatus.OK, response
