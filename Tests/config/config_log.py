import logging


def setup_logger(name="test_logger", log_level=logging.INFO, log_file=None):
    log = logging.getLogger(name)
    log.setLevel(log_level)

    if not log.hasHandlers():
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        log.addHandler(console_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            log.addHandler(file_handler)

    return log


logger = setup_logger(log_level=logging.DEBUG, log_file="test_logs.log")
