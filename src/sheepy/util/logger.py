"""Logging utility"""

import logging
import os
import sys

if not os.path.exists("logs"):
    os.mkdir("logs")
    if not os.path.exists("logs/file.log"):
        open("logs/file.log", "w").close()

LOG_FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(filename="logs/file.log"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)