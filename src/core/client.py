from log import log


class Client(object):

    def __init__(self):
        return

    def write(self, message):
        self.fd.write(message)

    def write_header(self, header):
        log.debug("%s\r\n" % header)
        self.write("%s\r\n" % header)
