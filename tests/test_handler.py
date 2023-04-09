import json

from lambda_function import lambda_handler


def test_handler():
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
    assert body["niall_output"].startswith("[dry] ")
