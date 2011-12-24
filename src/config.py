import os
from regexes import CONFIG_REGEX


class Config(object):
    """Configuration loader"""

    __data = {}

    def __init__(self, path):
        self.load_file(path)
        self.load_settings()

    def load_file(self, path):
        """Load up the config file"""
        if os.path.exists(path):
            self.__config = open(path, "r").read()

    def load_settings(self):
        """Start loading and setting config values"""
        for line in self.__config.split("\n"):
            line = line.strip()
            if not line or line[0] in ("\n", "#"):
                continue
            c = CONFIG_REGEX.search(line)
            if c:
                name = c.group("name").upper()
                value = c.group("value")
                if not value:
                    value = None
                self.set(name, value)

    def get(self, name):
        """Returns a single config value"""
        try:
            if self.__data[name]:
                return self.__data[name]
        except:
            return False

    def set(self, name, value):
        """Set a single config value"""
        self.__data[name] = value


config = Config("conf/aphttpd.conf")
