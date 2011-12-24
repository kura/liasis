#!/usr/bin/env python

import sys
import os
import eventlet
import socket
import logging

eventlet.monkey_patch()

HOST = "0.0.0.0"
PORT = 8080
MAX_CONNECTIONS = 10
LOG = "debug.log"

STATUS_CODES = {
    "1.0": {
    },
    "1.1": {
        100: "Continue",
        101: "Switching protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        306: "Unused - Reserved",
        307: "Temporary Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Unused - Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Request Entity Too Large",
        414: "Request-URI Too Long",
        415: "Unsupported Media Type",
        416: "Requested Range Not Satisfiable",
        417: "Expectation Failed",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
    },
}

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = "(%asctime)s %(message)s"

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOGGING_FORMAT)

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
stream.setFormatter(logging.Formatter("%(message)s"))

file_log = logging.FileHandler(LOG)
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
        log.debug(line)


def main():
    try:
        eventlet.serve(eventlet.listen((HOST, PORT)), handle,
                       concurrency=MAX_CONNECTIONS)
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
