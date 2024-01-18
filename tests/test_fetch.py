import httpx
import pytest
import json
from src import fetch, JSON


def test_fetch_is_working():
    res = fetch('https://www.google.com/')

    assert res.status_code == 200


def test_fetch_raise_exception_on_invalids_urls():
    with pytest.raises(httpx.ConnectError) as exception:
        fetch('https://www.should-be-a-non-existing-url.com/')

        assert isinstance(exception, httpx.ConnectError)


def test_fetch_returning_json():
    res = fetch('https://jsonplaceholder.typicode.com/todos/1')

    assert isinstance(res.json(), dict)


def test_fetch_post_method():
    res = fetch(
        'https://jsonplaceholder.typicode.com/posts', {
            'method':
                'POST',
            'body':
                JSON.stringify({
                    'title': 'foo',
                    'body': 'bar',
                    'userId': 1,
                }),
            'headers': {
                'Content-type': 'application/json; charset=UTF-8',
            }
        }
    )

    assert isinstance(res.json(), dict)


def test_fetch_delete_method():
    res = fetch(
        'https://jsonplaceholder.typicode.com/posts/1', {
            'method': 'DELETE',
        }
    )

    assert res.status_code == 200


def test_fetch_with_custom_method():
    res = fetch('https://www.google.com/', options={'method': 'post'})
    assert res.status_code == 405  # Assuming POST is not allowed on Google's homepage


def test_fetch_with_custom_headers():
    custom_headers = {'User-Agent': 'Custom-Agent'}
    res = fetch(
        'https://www.httpbin.org/headers', options={'headers': custom_headers}
    )
    assert res.json()['headers']['User-Agent'] == 'Custom-Agent'


def test_fetch_with_json_body():
    body_data = {'key': 'value'}
    res = fetch(
        'https://www.httpbin.org/post',
        options={
            'method': 'post',
            'body': JSON.stringify(body_data)
        }
    )
    assert res.json()['json'] == body_data


def test_fetch_without_body():
    res = fetch('https://www.httpbin.org/get', options={'method': 'get'})
    assert res.json()['args'] == {}


def test_fetch_with_invalid_json_body():
    with pytest.raises(json.JSONDecodeError):
        fetch(
            'https://www.google.com/',
            options={
                'method': 'post',
                'body': 'invalid json'
            }
        )
