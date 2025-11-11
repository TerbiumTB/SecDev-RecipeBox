import pytest
from pytest import FixtureRequest

from app.shared.limit import limiter


@pytest.fixture(autouse=True)
def control_rate_limiter(request: FixtureRequest):
    limiter.reset()

    limiter.enabled = "ratelimit" in request.keywords
    yield
    limiter.enabled = True
