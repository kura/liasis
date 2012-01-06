import os
from eventlet import hubs
from eventlet.greenio import GreenSocket
import eventlet
from liasis.core.server import Server
from liasis.config import config

server = Server()

class Worker(object):

    def __init__(self, sock):
        self.socket = sock

    def init_worker(self):
        hubs.use_hub()

    def run(self):
        self.socket = GreenSocket(family_or_realsock=self.socket.sock)
        self.socket.setblocking(1)
        self.acceptor = eventlet.spawn(eventlet.serve, self.socket, server.handle, int(config.get("MAX_CONNECTIONS")))
        while True:
            eventlet.sleep(0.1)
        with eventlet.Timeout(30, False):
            eventlet.kill(self.acceptor, eventlet.StopServe)
