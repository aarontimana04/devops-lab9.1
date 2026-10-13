import json
from urllib.parse import urlencode
import pytest
from handler import handler


def apigw_v2_event(path, query=None):
    return {
        "version": "2.0",
        "routeKey": f"GET {path}",
        "rawPath": path,
        "rawQueryString": urlencode(query or {}),
        "headers": {"host": "localhost"},
        "queryStringParameters": query or {},
        "requestContext": {
            "http": {"method": "GET", "path": path,
                     "sourceIp": "127.0.0.1", "protocol": "HTTP/1.1"},
            "stage": "$default",
        },
        "isBase64Encoded": False,
    }


class FakeContext:
    function_name = "api"
    memory_limit_in_mb = 128
    invoked_function_arn = "arn:aws:lambda:us-east-1:000000000000:function:api"
    aws_request_id = "test-request-id"


@pytest.mark.parametrize("name", ["Aaron", "María José", "A&B"])
def test_lambda_hello(name):
    response = handler(apigw_v2_event("/hello", {"name": name}), FakeContext())
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"message": f"Hello, {name}!", "source": "FastAPI"}
    assert response["headers"]["content-type"] == "application/json"


def test_lambda_add():
    response = handler(apigw_v2_event("/add", {"a": "2", "b": "3"}), FakeContext())
    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"result": 5}


def test_lambda_invalid_query():
    assert handler(apigw_v2_event("/add", {"a": "x", "b": "3"}),
                   FakeContext())["statusCode"] == 422


def test_lambda_unknown_route():
    assert handler(apigw_v2_event("/nope"), FakeContext())["statusCode"] == 404
