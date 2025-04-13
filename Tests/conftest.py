import pytest
from loguru import logger
import sys


def pytest_adoption(parser):
    parser.addoption(
        "--log-level-custom",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    )


@pytest.fixture(scope="session", autouse=True)
def setup_logging(request):
    log_level = request.config.getoption("--log-level-custom")
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: "
               "<8}</level> | <cyan>{name}</cyan>:<cyan>{function}"
               "</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )