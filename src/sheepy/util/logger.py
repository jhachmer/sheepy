"""Logging utility"""

import logging
import os
import sys

LOG_FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def create_log_dir(dir_name: str, log_file_name: str):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        if not os.path.exists(os.path.join(dir_name, log_file_name)):
            open(os.path.join(dir_name, log_file_name), "w").close()


def setup_logging(dir_name: str = "logs", log_file_name: str = "file.log"):
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(filename=os.path.join(dir_name, log_file_name)),
            logging.StreamHandler(stream=sys.stdout),
        ],
    )
    create_log_dir(dir_name=dir_name, log_file_name=log_file_name)
