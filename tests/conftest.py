import sys
from pathlib import Path


def pytest_configure(config):
    config.addinivalue_line("markers", "ratelimit: mark test to run with rate limiting")


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

pytest_plugins = ["fixtures.mock", "fixtures.rate_limit"]
