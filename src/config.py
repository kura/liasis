import os
from core.regexes import CONFIG, VHOST, WHITESPACE, NL


class Config(object):
    """Configuration loader"""

    __data = {}

    def __init__(self, path):
        self.load_file(path)
        self.load_settings()
        self.set('vhosts', Vhosts().get())

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
            c = CONFIG.search(line)
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


class Vhosts(object):
    
    __content = ""
    __data = {}
    
    def __init__(self):
        self.load_files()
        self.load_settings()

    def load_files(self):
        for hfile in os.listdir("sites"):
            self.__content += open("sites/"+hfile, "r").read()
        self.__content = WHITESPACE.sub(" ", self.__content)
        self.__content = NL.sub("", self.__content)

    def load_settings(self):
        vhosts = VHOST.findall(self.__content)
        for vhost in vhosts:
            print vhost.split(";")

    def get(self):
        return self.__data


config = Config("conf/liasis.conf")
