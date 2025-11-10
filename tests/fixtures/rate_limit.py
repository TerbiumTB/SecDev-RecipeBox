import pytest
from app.shared.limit import limiter
from pytest import FixtureRequest

@pytest.fixture(autouse=True)
def control_rate_limiter(request: FixtureRequest):
    limiter.reset()

    limiter.enabled = "ratelimit" in request.keywords
    yield
    limiter.enabled = True  
