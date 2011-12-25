import os
from datetime import datetime
from log import log
from routing import ROUTES
from core.status import STATUS_CODES
from core.regexes import HTTP_BASE, HTTP_HOST, CRNL


NOW = datetime.now()
FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


class Client(object):

    def __init__(self):
        return


class RequestHandler(object):

    done = False

    def __init__(self, client):
        self.c = client

    def handle(self, line):
        self.line = line
        h = HTTP_BASE.match(self.line)
        if h:
            self.rtype = h.group('type')
            self.dialect = h.group('dialect')
            self.uri = h.group('uri')
        h = HTTP_HOST.match(self.line)
        if h:
            self.full_host = h.group('host')
            self.host, self.host_port = self.full_host.split(":")
        if CRNL.match(self.line):
            self.done = True

def handle(sock, addr):
    c = Client()
    c.addr = addr
    c.fd = sock.makefile("rw")
    r = RequestHandler(c)

    while True:
        line = c.fd.readline()
        if not line:
            break
        log.debug(line.strip())
        r.handle(line)
        if r.done is True:
            print r.__dict__
            try:
                page = ROUTES[r.uri]
                return_code = 200
            except KeyError:
                page = "404"
                return_code = 404
            c.fd.write("\n\n")
            if r.uri == "/":
                for p in page:
                    if os.path.exists(p):
                        tfile = p
                        break
            if modified_date(tfile) < NOW:
                return_code = 304
            c.fd.write("HTTP/1.1 %s %s\n" % (return_code, STATUS_CODES['1.1'][return_code]))
            c.fd.write("Server: Liasis\n")
            c.fd.write("Date: %s\n" % NOW.strftime(FORMAT))
            c.fd.write("Last-Modified: %s\n" % modified_date(tfile).strftime(FORMAT))
            c.fd.write("\n")
            for piece in read_chunks(open(tfile, "r")):
                print piece
                c.fd.write(piece)
            return

def modified_date(tfile):
    return datetime.fromtimestamp(os.stat(tfile).st_mtime)

def read_chunks(file_obj, chunk=1024):
    while True:
        data = file_obj.read(chunk)
        if not data:
            break
        yield data