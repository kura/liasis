#!/usr/bin/env python

import sys
import os
import eventlet
import socket
import logging
from config import Config
from status import STATUS_CODES
from routing import ROUTES
eventlet.monkey_patch()


config = Config("aphttpd.conf")

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


def handle(sock, addr):
    fd = sock.makefile("rw")
    while True:
        line = fd.readline()
        if not line:
            break
        if line.lower().startswith("get"):
            fd.write(200)
            fd.write(open("index.html").read())
        log.debug(line)


def main():
    try:
        eventlet.serve(eventlet.listen((config.get("HOST"), int(config.get("PORT")))), handle,
                       concurrency=int(config.get("MAX_CONNECTIONS")))
    except socket.error as e:
        log.warn(e)
        eventlet.StopServer()
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        log.info("Stopping APHTTPD...")
        eventlet.StopServer()
        sys.exit(os.EX_OK)
