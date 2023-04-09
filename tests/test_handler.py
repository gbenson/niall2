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


@pytest.fixture
def mock_database(monkeypatch):
    session = MockBoto3Session()
    monkeypatch.setattr(boto3, "DEFAULT_SESSION", session)
    yield session
    session._tables[:] = []


@pytest.fixture
def deterministic():
    random.seed("Hello Niall")


def test_handler(mock_database, deterministic):
    response = lambda_handler({
        "body": json.dumps({
            "user_input": "Hello Niall",
            "dry_run": True,
        })}, None)

    assert "statusCode" in response
    assert response["statusCode"] == 200

    assert "headers" in response
    assert "Access-Control-Allow-Origin" in response["headers"]
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"

    assert "body" in response
    body = json.loads(response["body"])

    assert "niall_output" in body
    assert body["niall_output"] == ("[dry] hello gary")
