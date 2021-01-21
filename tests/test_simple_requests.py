import pytest
from requests.exceptions import Timeout

from safe_requests_session import SafeSession


def test_timeout_is_timeouting():
    s = SafeSession(max_retries=2, timeout=1)
    # non-routable IP address surely results in a timeout
    url = "http://10.255.255.1"
    with pytest.raises(Timeout):
        s.get(url)


def test_retries():
    pass
