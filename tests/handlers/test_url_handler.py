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
    dynamodb = boto3.resource('dynamodb', "us-east-1")
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
        _event = {
            "body": json.dumps({
                "url": "https://www.xxxx.com/blog/test.html",
                "title": "title link"
            })
        }

        response = url_handler.create_shortcode_handler(_event, None)
        assert response["statusCode"] == 201
        assert "shortcode" in json.loads(response["body"])

    @mock_dynamodb2
    def test_existing_short_code_handler(self, mocker):
        from src.handlers import url_handler
        expected = {
            "shortcode": "xxxxx"
        }

        create_table_mock()
        add_new_record({
            "id": "1111111",
            "url": "https://www.xxxx.com/blog/test.html",
            "title": "title link"
        })

        mocker.patch("src.controller.url_controller.to_base62", return_value="xxxxx")

        _event = {
            "body": json.dumps({
                "url": "https://www.xxxx.com/blog/test.html",
                "title": "title link"
            })
        }
        response = url_handler.create_shortcode_handler(_event, None)
        assert response["statusCode"] == 201
        body = json.loads(response["body"])
        assert body["shortcode"] == expected["shortcode"]
