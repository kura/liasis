import re


CONFIG_REGEX = re.compile(r"(?P<name>.*?)\s*[:=]\s*(?P<value>.*)")
