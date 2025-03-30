import pytest

@pytest.mark.timeout(10)  # Fail the test if it runs longer than 10 seconds
def test_function():
    ...

def test_hello_world():
    assert 1 + 1 == 2