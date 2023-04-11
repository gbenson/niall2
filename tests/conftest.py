import random

from decimal import Decimal

import boto3
import pytest


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
        self._responses = [
            {"Items": [
                {"From": "_", "To": "hello", "Weight": Decimal(1)},
                {"From": "_", "To": "abc", "Weight": Decimal(20)},
            ]},
            {"Items": [
                {"From": "hello", "To": "gary", "Weight": Decimal(123)},
            ]},
            {"Items": [
                {"From": "gary", "To": "_", "Weight": Decimal(23)},
                {"From": "gary", "To": "sucks", "Weight": Decimal(42)},
                {"From": "gary", "To": "pang", "Weight": Decimal(1)},
            ]},
        ]
        self._responses.append(self._responses[0])
        self._responses.extend([
            {"Items": [
                {"From": "abc", "To": "easy", "Weight": Decimal(1)},
            ]},
            {"Items": [
                {"From": "easy", "To": "as", "Weight": Decimal(1)},
            ]},
            {"Items": [
                {"From": "as", "To": "pie", "Weight": Decimal(9)},
                {"From": "as", "To": "123", "Weight": Decimal(9)},
            ]},
            {"Items": [
                {"From": "123", "To": "_", "Weight": Decimal(4)},
            ]},
        ])

    def load(self):
        self._load_count += 1

    def query(self, **kwargs):
        self._queries.append(kwargs)
        return self._responses[len(self._queries) - 1]


@pytest.fixture
def mock_database(monkeypatch, deterministic):
    session = MockBoto3Session()
    monkeypatch.setattr(boto3, "DEFAULT_SESSION", session)
    yield session


@pytest.fixture
def deterministic():
    random.seed("Hello Niall")
