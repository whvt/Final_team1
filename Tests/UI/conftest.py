import logging
import pytest
from Tests.utils.browser_manager import get_driver

@pytest.fixture(scope="module")
def driver():

    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()
@pytest.fixture(scope="session", autouse=True)
def configure_logging():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)


    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)


    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)


    if not logger.handlers:
        logger.addHandler(console_handler)


    yield


    logger.handlers.clear()