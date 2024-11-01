from sheepy.util.logger import setup_logging

# TODO: maybe move to env variable?
LOG_DIR = "logs"
LOG_FILE = "file.log"

setup_logging(LOG_DIR, LOG_FILE)
