import datetime
from log import log
from routing import ROUTES
from status import STATUS_CODES
from regexes import HTTP10_REGEX

now = datetime.datetime.now()

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
        fd.write("Date: %s\n" % now.strftime("%a, %m %b %Y %H:%M:%S %Z"))
        log.debug(line)
        fd.write("\n\nHi Kura")
        return
