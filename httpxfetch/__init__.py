import httpx
import json


class JSON:
    @classmethod
    def stringify(cls, data: dict):
        return json.dumps(data)


def fetch(url: str, options: dict = {}) -> httpx.Response:
    method = options.get('method', 'get')
    headers = options.get('headers', {})
    body = options.get('body', '')

    request_args = {
        'method': method,
        'url': url,
        'headers': headers,
    }

    if method not in ['get', 'head']:
        if body:
            request_args['content'] = JSON.stringify(
                json.loads(body) if isinstance(body, str) else body
            )

    res = httpx.request(**request_args)
    return res
