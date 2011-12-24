import os
from datetime import datetime
from log import log
from routing import ROUTES
from status import STATUS_CODES
from regexes import HTTP10_REGEX


NOW = datetime.now()
FORMAT = "%a, %m %b %Y %H:%M:%S %Z"

# TODO
#
# Fix because right now it's accepting the GET request
# and ignoring EVERYTHING after that line because it
# spits out it's status and content and closes connection

def handle(sock, addr):
    fd = sock.makefile("rw")
    while True:
        line = fd.readline()
        if not line:
            break
        if HTTP10_REGEX.match(line):
            log.debug("HTTP/1.0")
            fd.write("HTTP/1.1 500 %s" % STATUS_CODES['1.1'][505])
        if line.lower().startswith("get"):
            fd.write("HTTP/1.1 200 %s\n" % STATUS_CODES['1.1'][200])
        fd.write("Server: Asynchronous Python HTTP Daemon\n")
        fd.write("Date: %s\n" % NOW.strftime(FORMAT))
        fd.write("Last-Modified: %s\n" % modified_date("index.html"))
        log.debug(line)
        fd.write("\n\nHi Kura")
        return

def modified_date(file):
    return datetime.fromtimestamp(os.stat(file).st_mtime).strftime(FORMAT)
