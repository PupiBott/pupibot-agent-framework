# Testing Guide for Agent Runner

## Running Tests Locally

To run the tests for the `agent-runner` service, use the following command:

```bash
pytest -vv -s
```

### Notes on Mocking with `pytest-httpx`
- The `pytest-httpx` library is used to mock external HTTP calls.
- Mocks should match the exact request details, including:
  - **Method**: Ensure the HTTP method (e.g., `POST`) matches.
  - **URL**: Include the full URL, including port and path.
  - **Headers**: Explicitly match headers like `Content-Type` if required.
  - **Body**: Use `match_content=True` and provide the exact body content as bytes.

### Example Mock Setup
```python
httpx_mock.add_response(
    method="POST",
    url="http://document-service:8081/generate",
    json={"document": "ok"},
    match_content=True,
    content=b'{"payload":"test"}'
)
```

### Avoiding Flakiness
- Always use explicit content matching in mocks to prevent unexpected mismatches.
- Ensure the test database and environment variables are properly configured.

## CI Integration
- Ensure all tests pass locally before pushing changes.
- Include the regression test `test_external_call_matches_mock` to verify external call behavior.