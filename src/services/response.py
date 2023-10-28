import json

import jsonschema
from aws_lambda_powertools import Logger

from src.data.exceptions import BadRequestException
from src.services.config import ConfigService


class ResponseService:
    @staticmethod
    def pretty_response(func):
        """
        Decorator which generates the response to the api gateway request in json format
        :param func:
        :return:
        """
        def wrap(*args, **kwargs):
            conf_service = ConfigService()
            kwargs["conf_svc"] = conf_service
            logger = Logger(service=conf_service.LOGGER_SERVICE_NAME)
            kwargs["logger"] = logger

            headers = {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json"
            }
            try:
                status_code, response = func(*args, **kwargs)
            except jsonschema.exceptions.ValidationError as ex:
                logger.info({"message": "ValidationError ERROR", "exception": str(ex)})
                status_code = 400
                response = {'message': str(ex)}
            except jsonschema.exceptions.SchemaError as ex:
                logger.info({"message": "SchemaError ERROR", "exception": str(ex)})
                status_code = 400
                response = {'message': str(ex)}
            except BadRequestException as ex:
                logger.info({"message": "BadRequest ERROR", "exception": str(ex)})
                status_code = 400
                response = {'message': str(ex)}
            except Exception as ex:
                logger.info({"message": "Exception ERROR", "exception": str(ex)})
                status_code = 500
                response = {'message': str(ex)}
            response = json.dumps(response)
            return {"statusCode": status_code,  "headers": headers, "body": response}
        return wrap
