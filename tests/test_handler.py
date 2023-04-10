import json
import random

from decimal import Decimal

import boto3
import pytest

from lambda_function import lambda_handler


class MockBoto3Session:
    def __init__(self):
        self._tables = []

    def resource(self, *args, **kwargs):
        return MockDynamoDBResource(self, *args, **kwargs)


class MockDynamoDBResource:
    def __init__(self, session, service_name):
        self._session = session
        self._service_name = service_name

    def Table(self, *args, **kwargs):
        return MockDynamoDBTable(self, *args, **kwargs)


class MockDynamoDBTable:
    def __init__(self, resource, name):
        self._resource = resource
        self._resource._session._tables.append(self)
        self._name = name
        self._load_count = 0
        self._queries = []

    def load(self):
        self._load_count += 1

    def query(self, **kwargs):
        self._queries.append(kwargs)
        return self._responses[len(self._queries) - 1]

    _responses = [
        {"Items": [
            {"From": "_", "To": "hello", "Weight": Decimal(5)},
            {"From": "_", "To": "abc", "Weight": Decimal(16)},
            ],
         },
        {"Items": [
            {"From": "hello", "To": "gary", "Weight": Decimal(123)},
            ],
         },
        {"Items": [
            {"From": "gary", "To": "_", "Weight": Decimal(23)},
            {"From": "gary", "To": "sucks", "Weight": Decimal(42)},
            {"From": "gary", "To": "pang", "Weight": Decimal(1)},
            ],
         },
    ]


@pytest.fixture(scope="class")
def mock_database():
    session = MockBoto3Session()
    saved_session = boto3.DEFAULT_SESSION
    boto3.DEFAULT_SESSION = session
    try:
        yield session
    finally:
        boto3.DEFAULT_SESSION = saved_session
        session._tables[:] = []


@pytest.fixture(scope="class")
def deterministic():
    random.seed("Hello Niall")


class TestHandler:
    @pytest.fixture(scope="class")
    def response(self, mock_database, deterministic):
        return lambda_handler({
            "body": json.dumps({
                "user_input": "Hello Niall",
                "dry_run": True,
            })}, None)

    def test_response_has_status(self, response):
        assert "statusCode" in response

    def test_response_status(self, response):
        assert response["statusCode"] == 200

    def test_response_has_headers(self, response):
        assert "headers" in response

    def test_response_has_cors_headers(self, response):
        assert "Access-Control-Allow-Origin" in response["headers"]

    def test_cors_headers(self, response):
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"

    def test_response_has_body(self, response):
        assert "body" in response

    @pytest.fixture(scope="class")
    def response_body(self, response):
        return json.loads(response["body"])

    def test_body_has_niall_output(self, response_body):
        assert "niall_output" in response_body

    def test_niall_output(self, response_body):
        assert response_body["niall_output"] == "[dry] hello gary"
