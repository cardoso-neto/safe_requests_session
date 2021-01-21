"""
A requests session that retries on errors and timeouts instead of hanging.

Adapted from:
https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/

Usage:
# try:
#     r = SafeSession().get("http://localhost:80")
#     r.raise_for_status()
# except requests.exceptions.HTTPError as e:
#     print("Http Error:", e)
# except requests.exceptions.ConnectionError as e:
#     print("Error Connecting:", e)
# except requests.exceptions.Timeout as e:
#     print("Timeout Error:", e)
# except requests.exceptions.RequestException as e:
#     print("OOps: something else", e)

requests Exception treatment source:
https://stackoverflow.com/questions/16511337/correct-way-to-try-except-using-python-requests-module

"""
from typing import List, Optional, Union

from requests import PreparedRequest, Response, Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, timeout: int = 16, **kwargs):
        self.timeout = timeout
        super().__init__(*args, **kwargs)

    def send(
        self, request: PreparedRequest, timeout: Optional[int] = None, **kwargs
    ) -> Response:
        if timeout is None:
            kwargs["timeout"] = self.timeout
        else:
            kwargs["timeout"] = timeout
        return super().send(request, **kwargs)


class SafeSession(Session):
    def __init__(
        self,
        max_retries: int = 3,
        timeout: int = 16,
        backoff_factor: Union[float, int] = 1,
        error_codes: Optional[List[int]] = None,
    ) -> None:
        super().__init__()
        if error_codes is None:
            error_codes = [413, 429, 500, 502, 503, 504]
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=error_codes,
            # allowed_methods=("GET", )  # careful here, only idempotent methods
        )
        adapter = TimeoutHTTPAdapter(timeout=timeout, max_retries=retry_strategy)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

