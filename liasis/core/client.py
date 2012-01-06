import os
from liasis.log import log


class Client(object):

    def __init__(self):
        return

    def write(self, message):
        self.fd.write(message)

    def write_header(self, header):
        log.debug("%s: %s\r\n" % (os.getpid(), header))
        self.write("%s\r\n" % header)
