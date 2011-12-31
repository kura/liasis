import re


CONFIG = re.compile(r"(?P<name>[a-z0-9\_]*)\s*(?P<value>.*);")
INCLUDE = re.compile(r"[^\#]include\s*\"(?P<file>[^\0]+)\";")
ASTERISK = re.compile(r"\*$")
WHITESPACE = re.compile(r"\s\s")
VHOST = re.compile(r"[^\#]server\s\{([^\#].*)\}")
HTTP_BASE = re.compile(r"(?P<type>GET|POST|HEAD)\s(?P<uri>.*)\sHTTP\/(?P<dialect>1\.(0|1))")
HTTP_HOST = re.compile(r"Host\:\s(?P<host>[a-z0-9\.\-\:]*)")
MODIFIED_SINCE = re.compile(r"If-Modified-Since:\s(?P<date>[a-zA-Z]{3}\,\s[0-9]{1,2}\s[a-zA-Z]{3}\s[0-9]{4}\s[0-9]{2}\:[0-9]{2}\:[0-9]{2})")
CRNL = re.compile(r"^\r\n$")
NL = re.compile(r"\n")
