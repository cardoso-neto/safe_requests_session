# Safe Requests Session
> A requests session that retries on errors and timeouts instead of hanging.

## Installing

`pip install git+https://github.com/cardoso-neto/safe_requests_session.git@master`

## Using

```python
# URL to retrieve one's own IP in a JSON.
url = "https://httpbin.org/ip"
session = SafeSession(max_retries=3, timeout=8)
response = session.get(url)
print(response.json())
# {'origin': '200.100.64.36'}
```

## Testing/Contributing

`git clone git@github.com:cardoso-neto/password_based_encryption.git`

`pip install -r requirements-test.txt`

`pip install -e .`

`pytest -v`
