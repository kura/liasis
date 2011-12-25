import re


CONFIG = re.compile(r"(?P<name>.*?)\s*[:=]\s*(?P<value>.*)")
HTTP_BASE = re.compile(r"(?P<type>GET|POST|HEAD)\s(?P<uri>.*)\sHTTP\/(?P<dialect>1\.(0|1))")
HTTP_HOST = re.compile(r"Host\:\s(?P<host>[a-z0-9\.\-\:]*)")
END_NL = re.compile(r"^\r\n$")