from urllib.parse import urlparse, urljoin

import json as json_lib
from threading import Lock

from requests.adapters import HTTPAdapter
from requests.models import Request
from requests.sessions import Session
from wilder.errors import WildClientError
from wilder.server import get_server_logger
from wilder.util import format_dict

SESSION_ADAPTER = HTTPAdapter(pool_connections=200, pool_maxsize=4, pool_block=True)
ROOT_SESSION = Session()
ROOT_SESSION.mount(u"https://", SESSION_ADAPTER)
ROOT_SESSION.mount(u"http://", SESSION_ADAPTER)
ROOT_SESSION.headers = {
    u"Accept": u"application/json",
    u"Content-Type": u"application/json",
    u"Accept-Encoding": u"gzip, deflate",
    u"Connection": u"keep-alive",
}


class Connection(object):
    def __init__(self, host, session=None):
        self._session = session or ROOT_SESSION
        self._headers = self._session.headers.copy()
        if not host.startswith(u"http://") and not host.startswith(u"https://"):
            host = u"https://{}".format(host)
        parsed_host = urlparse(host)
        self._headers[u"Host"] = parsed_host.netloc
        self.host_address = host

    def get(self, url, **kwargs):
        return self.request(u"GET", url, **kwargs)

    def options(self, url, **kwargs):
        return self.request(u"OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        return self.request(u"HEAD", url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.request(u"POST", url, data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(u"PUT", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(u"PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(u"DELETE", url, **kwargs)

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
            )

            if not stream and response is not None:
                # setting this manually speeds up read times
                response.encoding = u"utf-8"

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

        _print_request(method, url, params=params, data=data)
        return self._session.prepare_request(request)


def _handle_error(method, url, response):
    if response is None:
        msg = u"No response was returned for {} request to {}.".format(method, url)
        raise WildClientError(msg)


def _print_request(method, url, params=None, data=None):
    logger = get_server_logger()
    logger.info(u"{}{}".format(method.ljust(8), url))
    if params:
        logger.debug(format_dict(params, u"  params"))
    if data:
        logger.debug(format_dict(data, u"  data"))


def _create_connection(host_address="127.0.0.1", port=443):
    return Connection(f"{host_address}:{port}")


class WildClient:
    def __init__(self, connection=None):
        self.connection = connection or _create_connection("127.0.0.1, 5000")
        
    def get_artists(self):
        return []
