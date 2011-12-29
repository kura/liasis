import re


CONFIG = re.compile(r"(?P<name>.*?)\s*[:=]\s*(?P<value>.*)")
WHITESPACE = re.compile(r"\s\s")
VHOST = re.compile(r"server \{(.*)\}")
HTTP_BASE = re.compile(r"(?P<type>GET|POST|HEAD)\s(?P<uri>.*)\sHTTP\/(?P<dialect>1\.(0|1))")
HTTP_HOST = re.compile(r"Host\:\s(?P<host>[a-z0-9\.\-\:]*)")
MODIFIED_SINCE = re.compile(r"If-Modified-Since: \([^;]+\)\(\(; length=\([0-9]+\)$\)\|$\)")
CRNL = re.compile(r"^\r\n$")
NL = re.compile(r"\n")