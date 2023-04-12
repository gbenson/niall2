import pytest

from lambda_function import Robot


BASIC_REQUEST = {"body": '{"user_input": "Hello Niall"}'}, None
DRY_REQUEST = {"body": '{"user_input": "Hello Niall", "dry_run": true}'}, None
WET_REQUEST = {"body": '{"user_input": "Hello Niall", "dry_run": false}'}, None
EMPTY_REQUEST_1 = {"body": '{"user_input": ""}'}, None
EMPTY_REQUEST_2 = {"body": '{}'}, None


def test_response_status(mock_database):
    response = Robot()(*BASIC_REQUEST)
    assert response["statusCode"] == 200


def test_cors_headers(mock_database):
    response = Robot()(*BASIC_REQUEST)
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"


@pytest.mark.parametrize(
    "test_request,expect_body",
    ((BASIC_REQUEST, '{"niall_output": "hello gary"}'),
     (WET_REQUEST, '{"niall_output": "hello gary"}'),
     (DRY_REQUEST, '{"niall_output": "[dry] hello gary"}'),
     ))
def test_niall_output(mock_database, test_request, expect_body):
    response = Robot()(*test_request)
    assert response["body"] == expect_body


@pytest.mark.parametrize(
    "test_request,expect_num_updates",
    ((BASIC_REQUEST, 3),
     (WET_REQUEST, 3),
     (DRY_REQUEST, 0),
     (EMPTY_REQUEST_1, 0),
     (EMPTY_REQUEST_2, 0),
     ))
def test_num_updates(mock_database, test_request, expect_num_updates):
    Robot()(*test_request)
    assert len(mock_database._tables[0]._updates) == expect_num_updates
