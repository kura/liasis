import os
import sys
import argparse
from liasis import SERVER_SOFTWARE


parser = argparse.ArgumentParser(description="Liasis HTTPD", prog="liasis")
parser.add_argument("-c", "--conf", action="store", dest="conf", nargs=1,
                   required=True, help="Liasis primary configuration file",
                   type=argparse.FileType("r"))
parser.add_argument("-v", "--version", action="version", version=SERVER_SOFTWARE)

args = parser.parse_args()
