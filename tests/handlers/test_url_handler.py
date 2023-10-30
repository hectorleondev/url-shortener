import json

import boto3
import pytest
from moto import mock_dynamodb2

from src.data.model.url import UrlModel


def create_table_mock():
    conn = boto3.client("dynamodb", "us-east-1")
    conn.create_table(
        TableName="url_table",
        KeySchema=[
            {"AttributeName": "url_id", "KeyType": "HASH"},
        ],
        AttributeDefinitions=[
            {"AttributeName": "url_id", "AttributeType": "N"},
            {"AttributeName": "url_path", "AttributeType": "S"},
        ],
        BillingMode="PAY_PER_REQUEST",
        GlobalSecondaryIndexes=[
            {
                "IndexName": "url_path_index",
                "KeySchema": [{"AttributeName": "url_path", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
            },
        ],
    )


def add_new_record(item):
    dynamodb = boto3.resource("dynamodb", "us-east-1")
    table = dynamodb.Table("url_table")
    url_model = UrlModel()
    url_model.url_id = item["id"]
    url_model.url_path = item["url"]
    url_model.url_title = item["title"]
    url_model.save()


class TestUrlHandler:
    @mock_dynamodb2
    def test_new_create_shortcode_handler(self):
        from src.handlers import url_handler

        create_table_mock()
        _event = {"body": json.dumps({"url": "https://www.xxxx.com/blog/test.html"})}

        response = url_handler.create_shortcode_handler(_event, None)
        assert response["statusCode"] == 201
        assert "shortcode" in json.loads(response["body"])

    @mock_dynamodb2
    def test_existing_short_code_handler_error(self, mocker):
        from src.handlers import url_handler

        expected = {"message": "The url is already used for another short link"}

        create_table_mock()
        add_new_record(
            {
                "id": "1111111",
                "url": "https://www.xxxx.com/blog/test.html",
                "title": "title link",
            }
        )

        mocker.patch("src.controller.url_controller.to_base62", return_value="xxxxx")

        _event = {
            "body": json.dumps(
                {"url": "https://www.xxxx.com/blog/test.html", "title": "title link"}
            )
        }
        response = url_handler.create_shortcode_handler(_event, None)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == expected

    def test_invalid_url_error(self, mocker):
        from src.handlers import url_handler

        _event = {
            "body": json.dumps(
                {"url": "http/www.xxxx.com/blog/test.html", "title": "title link"}
            )
        }
        response = url_handler.create_shortcode_handler(_event, None)
        assert response["statusCode"] == 400

    @mock_dynamodb2
    def test_retrieve_url_data(self, mocker):
        from src.handlers import url_handler

        expected = {"url": "https://www.xxxx.com/blog/test.html", "title": "title link"}
        create_table_mock()
        add_new_record(
            {
                "id": 1111111,
                "url": "https://www.xxxx.com/blog/test.html",
                "title": "title link",
            }
        )

        _event = {"queryStringParameters": {"shortcode": "xxxxx"}}

        mocker.patch("src.controller.url_controller.to_base10", return_value=1111111)

        response = url_handler.retrieve_url_data_handler(_event, None)
        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert body["url"] == expected["url"]
        assert body["title"] == expected["title"]
        assert "created_at" in body

    @mock_dynamodb2
    def test_invalid_shortcode_processing_error(self, mocker):
        from src.handlers import url_handler

        create_table_mock()
        expected = {
            "message": "The shortcode is invalid",
        }

        _event = {"queryStringParameters": {"shortcode": "AF643$"}}

        response = url_handler.retrieve_url_data_handler(_event, None)
        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert body == expected

    def test_invalid_shortcode_validation_error(self, mocker):
        from src.handlers import url_handler

        _event = {"queryStringParameters": {}}

        response = url_handler.retrieve_url_data_handler(_event, None)
        assert response["statusCode"] == 400

    @mock_dynamodb2
    def test_retrieve_existing_short_code_handler(self, mocker):
        from src.handlers import url_handler

        expected = {"shortcode": "xxxxx"}

        create_table_mock()
        add_new_record(
            {
                "id": "1111111",
                "url": "https://www.xxxx.com/blog/test.html",
                "title": "title link",
            }
        )

        mocker.patch("src.controller.url_controller.to_base62", return_value="xxxxx")

        _event = {
            "queryStringParameters": {"url": "https://www.xxxx.com/blog/test.html"}
        }
        response = url_handler.retrieve_shortcode_handler(_event, None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == expected

    @mock_dynamodb2
    def test_retrieve_existing_short_code_not_found_url_error(self, mocker):
        from src.handlers import url_handler

        expected = {"message": "The url not found"}

        create_table_mock()
        add_new_record(
            {
                "id": "1111111",
                "url": "https://www.xxxx.com/blog/test.html",
                "title": "title link",
            }
        )

        _event = {
            "queryStringParameters": {"url": "https://www.xxxx.com/blog/test_two.html"}
        }
        response = url_handler.retrieve_shortcode_handler(_event, None)
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == expected

    @mock_dynamodb2
    def test_retrieve_existing_short_code_validation_error(self, mocker):
        from src.handlers import url_handler

        create_table_mock()
        add_new_record(
            {
                "id": "1111111",
                "url": "https://www.xxxx.com/blog/test.html",
                "title": "title link",
            }
        )

        _event = {"queryStringParameters": {}}
        response = url_handler.retrieve_shortcode_handler(_event, None)
        assert response["statusCode"] == 400
