import pytest
from requests.exceptions import RetryError, Timeout

from safe_requests_session import SafeSession


def test_timeout_is_timeouting():
    s = SafeSession(max_retries=0, timeout=1)
    # non-routable IP address surely results in a timeout
    url = "http://10.255.255.1"
    with pytest.raises(Timeout):
        s.get(url)


def test_retries():
    s = SafeSession(max_retries=1, backoff_factor=0.1, error_codes=[503])
    # address that always returns 503
    url = "https://httpbin.org/status/503"
    with pytest.raises(RetryError):
        s.get(url)
