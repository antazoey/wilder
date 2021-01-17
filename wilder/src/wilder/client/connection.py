import json as json_lib
from json import JSONDecodeError
from urllib.parse import urljoin
from urllib.parse import urlparse

from requests.adapters import HTTPAdapter
from requests.models import Request
from requests.sessions import Session
from wilder.client.errors import WildBadRequestError
from wilder.client.errors import WildClientError
from wilder.client.errors import WildNotFoundError
from wilder.client.errors import WildUnknownServerError
from wilder.lib.errors import ArtistNotFoundError
from wilder.lib.config import get_config_json
from wilder.lib.constants import Constants


SESSION_ADAPTER = HTTPAdapter(pool_connections=200, pool_maxsize=4, pool_block=True)
ROOT_SESSION = Session()
ROOT_SESSION.mount("https://", SESSION_ADAPTER)
ROOT_SESSION.mount("http://", SESSION_ADAPTER)
ROOT_SESSION.headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def create_connection():
    _config = get_config_json()
    host = _config.get(Constants.HOST, Constants.DEFAULT_HOST)
    port = _config.get(Constants.PORT, Constants.DEFAULT_PORT)
    return Connection(f"{host}:{port}")


class Connection:
    def __init__(self, host, session=None):
        self._session = session or ROOT_SESSION
        self._headers = self._session.headers.copy()
        if not host.startswith("http://") and not host.startswith("https://"):
            host = f"https://{host}"
        parsed_host = urlparse(host)
        self._headers["Host"] = parsed_host.netloc
        self.host_address = host

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def options(self, url, **kwargs):
        return self.request("OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        return self.request("HEAD", url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.request("POST", url, data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        json=None,
        cookies=None,
        files=None,
        hooks=None,
        stream=False,
        timeout=60,
        cert=None,
        proxies=None,
    ):
        response = None
        for _ in range(2):
            request = self._prepare_request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                cookies=cookies,
                files=files,
                hooks=hooks,
            )

            response = self._session.send(
                request,
                stream=stream,
                timeout=timeout,
                cert=cert,
                proxies=proxies,
                verify=False,
            )

            if not stream and response is not None:
                # setting this manually speeds up read times
                response.encoding = "utf-8"

            if response is not None and 200 <= response.status_code <= 399:
                return response

        # if nothing has been returned after two attempts, something went wrong
        _handle_error(method, url, response)

    def _prepare_request(
        self,
        method,
        url,
        params=None,
        data=None,
        json=None,
        cookies=None,
        files=None,
        hooks=None,
    ):
        url = urljoin(self.host_address, url)

        if json is not None:
            data = json_lib.dumps(json)

        request = Request(
            method=method,
            url=url,
            headers=self._headers,
            files=files,
            data=data,
            params=params,
            cookies=cookies,
            hooks=hooks,
        )
        return self._session.prepare_request(request)


def _handle_error(method, url, response):
    if response is None:
        msg = f"No response was returned for {method} request to {url}."
        raise WildClientError(msg)

    response_data = _try_get_response_data(response)
    if response.status_code == 400:
        raise WildBadRequestError(response_data)
    elif response.status_code == 404:
        _data_for_check = response_data.lower()
        if "not found" in _data_for_check:
            if "artist" in _data_for_check:
                raise ArtistNotFoundError(response_data)
        raise WildNotFoundError(response_data)
    raise WildUnknownServerError(response_data)


def _try_get_response_data(response):
    try:
        response_json = json_lib.loads(response.content)
    except JSONDecodeError:
        return str(response)
    return response_json.get("message") or str(response)
