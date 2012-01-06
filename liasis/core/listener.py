import sys
import socket
import eventlet
from eventlet.greenio import GreenSocket
from eventlet import hubs
from eventlet import debug
from liasis.config import config
eventlet.monkey_patch()
debug.hub_prevent_multiple_readers(False)


#s = eventlet.listen((
#                     config.get("HOST"), 
#                     int(config.get("PORT")), 
#                     ))
pool = eventlet.GreenPool(size=int(config.get("MAX_CONNECTIONS")))


class Listen(object):

    def __init__(self):
        self.host = config.get("HOST")
        self.port = int(config.get("PORT"))
        self.backlog = int(config.get("BACKLOG"))
        self.sock = None
	hubs.use_hub()

#    def open_socket(self):
#        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#        self.sock = GreenSocket(s)
#        self.sock.bind((self.host, self.port))
#        self.sock.listen(self.backlog)

    def open_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.sock = GreenSocket(family_or_realsock=s)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock = GreenSocket(s)
            self.sock.setblocking(1)
            self.sock.bind((self.host, self.port))
            self.sock.listen(50)
        except socket.error:
            if self.sock:
                self.close_socket()
            sys.exit(1)

    def close_socket(self):
        if self.sock:
            self.sock.close()
        sys.exit(1)


listener = Listen()
listener.open_socket()
