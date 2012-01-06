import sys
import logging
from liasis.config import config


LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = "%(message)s"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGGING_FORMAT)

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
stream.setFormatter(logging.Formatter("%(message)s"))

file_log = logging.FileHandler(config.get("LOG"))
file_log.setLevel(logging.DEBUG)
file_log.setFormatter(formatter)

log.addHandler(stream)
log.addHandler(file_log)

