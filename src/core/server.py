import os
import time
from mimetypes import MimeTypes
from datetime import datetime
from log import log
from core.status import STATUS_CODES
from core.regexes import HTTP_BASE, HTTP_HOST, CRNL, MODIFIED_SINCE
from core.listener import pool
import eventlet
eventlet.monkey_patch()


NOW = datetime.now()
FORMAT = "%a, %d %b %Y %H:%M:%S %Z"


class Client(object):

    def __init__(self):
        return
    
    def write(self, message):
        self.fd.write(message)
        
    def write_header(self, header):
        self.write("%s\r\n" % header)


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
            host_bits = self.full_host.split(":")
            self.host = host_bits[0]
            if len(host_bits) > 1:
                self.port = host_bits[1]
        if CRNL.match(self.line):
            self.done = True
        #if MODIFIED_SINCE.search(self.line):
            #m = MODIFIED_SINCE.match(self.line)
            #self.modified_since = m.group('date')
        #else:
            #self.modified_since = False


class Server(object):
    
    rc = 404
    tfile = "errors/404.html"

    def handle(self, sock, addr):
        self.c = Client()
        self.c.addr = addr
        self.c.fd = sock.makefile("rw")
        self.r = RequestHandler(self.c)

        while True:
            line = self.c.fd.readline()
            if not line:
                break
            log.debug(line.strip())
            self.r.handle(line)
            if self.r.done is True:
                break
        if self.r.uri == "/status":
            self.status()
            return
        if self.r.uri == "/":
            for p in ("index.htm", "index.html"):
                if os.path.exists(p):
                    self.tfile = p
                    self.rc = 200
                    break
        elif os.path.exists(os.path.join(os.getcwd(), self.r.uri[1:])):
            self.rc = 200
            self.tfile = self.r.uri[1:]
#        if r.modified_since is not False and modified_date(tfile) > r.modified_since:
#            return_code = 304
        self.headers()
        for piece in self.read_chunks(open(self.tfile, "r")):
            self.c.write(piece)
        return
    
    def headers(self):
        self.c.write_header("HTTP/1.1 %s %s" % (self.rc, STATUS_CODES['1.1'][self.rc]))
        self.c.write_header("Server: Liasis")
        self.c.write_header("Date: %s" % NOW.strftime(FORMAT))
        self.c.write_header("Last-Modified: %s" % self.modified_date().strftime(FORMAT))
        self.c.write_header("Content-Type: %s" % self.mime_type())
        self.c.write_header("Content-Length: %d" % self.filesize())
        self.c.write_header("X-XSS-Protection: 1; mode=block")
        self.c.write_header("X-Frame-Options: SAMEORIGIN")
        self.c.write("\r\n")

    def status(self):
        self.c.write_header("HTTP/1.1 %s %s" % (self.rc, STATUS_CODES['1.1'][self.rc]))
        self.c.write_header("Server: Liasis")
        self.c.write_header("Date: %s" % NOW.strftime(FORMAT))
        self.c.write("\r\n")
        self.c.write("Server: Liasis 0.0.0.1a\nUptime: NaN\n\n----------\n\nFree: %s\nRunning: %s\nWaiting: %s\n\n" % (pool.free(), pool.running(), pool.waiting()))
        dots = ""
        total = pool.free() + pool.running() + pool.waiting()
        not_free = pool.running() + pool.waiting()
        for i in range(pool.running()):
            dots += "R"
        for i in range(pool.waiting()):
            dots += "W"
        for i in range(total - not_free):
            dots += "."
        for i in range(total):
            if not i % 50:
                self.c.write("\n")
            self.c.write(dots[i])

    def modified_date(self):
        return datetime.fromtimestamp(os.stat(self.tfile).st_mtime)

    def read_chunks(self, file_obj, chunk=1024):
        while True:
            data = file_obj.read(chunk)
            if not data:
                break
            yield data

    def mime_type(self):
        m = MimeTypes()
        m.read("mime.types")
        if m.guess_type(self.tfile):
            return m.guess_type(self.tfile)[0]
        else:
            return "text/plain"

    def filesize(self):
        return os.path.getsize(self.tfile)
