import os
from core.regexes import HTTP_BASE, HTTP_HOST, CRNL, MODIFIED_SINCE 


class RequestHandler(object):

    done = False
    modified_since = None

    def __init__(self, client):
        self.c = client

    def handle(self, line):
        self.line = line
        h = HTTP_BASE.match(self.line)
        if h:
            self.rtype = h.group('type')
            self.dialect = h.group('dialect')
            self.uri = h.group('uri')
        if HTTP_HOST.match(self.line):
            h = HTTP_HOST.match(self.line)
            if h:
                self.full_host = h.group('host')
                host_bits = self.full_host.split(":")
                self.host = host_bits[0]
                if len(host_bits) > 1:
                    self.port = host_bits[1]
        if MODIFIED_SINCE.search(self.line):
            m = MODIFIED_SINCE.match(self.line)
            self.modified_since = m.group('date')
        if CRNL.match(self.line):
            self.done = True
    
