import os
from core.regexes import CONFIG, INCLUDE, ASTERISK, VHOST, WHITESPACE, NL


class Config(object):
    """Configuration loader"""

    __data = {}
    __includes = []
    __vhosts = []

    def __init__(self, path):
        self.__includes.append(path)
        self.find_includes(path)
        self.__config = ""
        for include in self.__includes:
            self.__config += "\n"+open(include, "r").read()+"\n"
        self.load_settings()
        self.vhosts()
        print self.__data, self.__includes, self.__vhosts

    def load_file(self, path):
        """Load up the config file"""
        if os.path.exists(path):
            self.__config = open(path, "r").read()

    def load_files(self, default):
        if os.path.exists(default):
            self.__includes.append(default)
            self.__config = open(default, "r").read()

    def find_includes(self, cfile):
        content = open(cfile, "r").read()
        includes = INCLUDE.findall(content)
        lincludes = []
        if includes > 0:
            for include in includes:
                if ASTERISK.search(include):
                    (path, asterisk) = os.path.split(include)
                    for efile in os.listdir(path):
                        fp = os.path.join(path, efile)
                        if os.path.exists(fp):
                            lincludes.append(fp)
                            self.__includes.append(fp)
                elif os.path.exists(include):
                    lincludes.append()
                    self.__includes.append(include)
        for i in lincludes:
            self.find_includes(i)

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

    def vhosts(self):
        content = WHITESPACE.sub(" ", self.__config)
        content = NL.sub("", content)
        vhosts = VHOST.findall(content)
        if len(vhosts) > 0:
            for vhost in vhosts:
                self.__vhosts.append(vhost.split(";"))


config = Config("conf/liasis.conf")
