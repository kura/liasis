from log import log


def handle(sock, addr):
    fd = sock.makefile("rw")
    while True:
        line = fd.readline()
        if not line:
            break
        if line.lower().startswith("get"):
            fd.write(200)
            fd.write(open("index.html").read())
        log.debug(line)

