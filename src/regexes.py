import re


CONFIG_REGEX = re.compile(r"(?P<name>.*?)\s*[:=]\s*(?P<value>.*)")
HTTP10_REGEX = re.compile(r"(.*)HTTP\/1\.0")
