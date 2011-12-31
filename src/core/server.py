import os
import time
from mimetypes import MimeTypes
from datetime import datetime
from log import log
from core.status import STATUS_CODES
from core.listener import pool
from core.defaults import *
from core.client import Client
from core.request import RequestHandler
import eventlet
eventlet.monkey_patch()


class Server(object):
    
    rc = 404
    tfile = "errors/404.html"

    def handle(self, sock, addr):
        self.NOW = datetime.now()
        try:
            os.chdir("/home/kura/workspace/liasis/iamkura.com/")
            self.c = Client()
            self.c.addr = addr
            self.c.fd = sock.makefile("rw")
            self.r = RequestHandler(self.c)

            while True:
                line = self.c.fd.readline()
                if not line:
                    break
                log.debug(line)
                self.r.handle(line)
                if self.r.done is True:
                    break
            if self.r.uri == "/liasis-status":
                self.status()
                return
            if self.r.uri == "/":
                for p in DIR_INDEX:
                    if os.path.exists(p):
                        self.tfile = p
                        self.rc = 200
                        break
            elif os.path.exists(os.path.join(os.getcwd(), self.r.uri[1:])):
                self.rc = 200
                self.tfile = self.r.uri[1:]
            if self.r.modified_since is not None and self.modified_date() > datetime.strptime(self.r.modified_since, IN_FORMAT):
                self.rc = 304

            self.tfile = os.path.join(os.getcwd(), self.tfile)
            self.headers()

            for piece in self.read_chunks(open(self.tfile, "r")):
                self.c.write(piece)
            return
        except Exception as e:
            log.debug(e)
   
    def headers(self):
        self.c.write_header("HTTP/1.1 %s %s" % (self.rc, STATUS_CODES['1.1'][self.rc]))
        self.c.write_header("Server: Liasis")
        self.c.write_header("Date: %s" % self.NOW.strftime(OUT_FORMAT))
        self.c.write_header("Last-Modified: %s" % self.modified_date().strftime(OUT_FORMAT))
        self.c.write_header("Content-Type: %s" % self.mime_type())
        self.c.write_header("Content-Length: %d" % self.filesize())
        self.c.write_header("X-XSS-Protection: 1; mode=block")
        self.c.write_header("X-Frame-Options: SAMEORIGIN")
        self.c.write("\r\n")

    def status(self):
        self.c.write_header("HTTP/1.1 200 %s" % (STATUS_CODES['1.1'][200]))
        self.c.write_header("Server: Liasis")
        self.c.write_header("Date: %s" % self.NOW.strftime(OUT_FORMAT))
        self.c.write("\r\n")
        self.c.write("Server: Liasis 0.0.0.1a\n")
        self.c.write("Uptime: NaN\n")
        self.c.write("Date: %s" % self.NOW.strftime(OUT_FORMAT))
        self.c.write("\n\n--------------------------------------------------\n\n")
        self.c.write("Free: %s | Running: %s | Waiting: %s\n" % (pool.free(), pool.running(), pool.waiting()))
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
        return

    def modified_date(self):
        mtime = str(os.path.getmtime(self.tfile)).split(".")[0]
        return datetime.fromtimestamp(float(mtime))

    def read_chunks(self, file_obj, chunk=1024):
        while True:
            data = file_obj.read(chunk)
            if not data:
                break
            yield data

    def mime_type(self):
        m = MimeTypes()
        m.read(LIASIS_DIR+MIME_TYPES)
        if m.guess_type(self.tfile):
            return m.guess_type(self.tfile)[0]
        else:
            return "text/plain"

    def filesize(self):
        return os.path.getsize(self.tfile)
