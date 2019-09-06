import argparse
from random import Random
from functools import partial
from http.server import HTTPServer

from .DBHack import DBHack
from .NoddyHandler import NoddyHandler

# Parse command line
parser = argparse.ArgumentParser(
    prog='noddyserver',
    description='Demo of license database',
)
parser.add_argument('dsn', metavar='DSN')
parser.add_argument('port', metavar='PORT', type=int)
args = parser.parse_args()

# Start server
db = DBHack(args.dsn)
port = args.port
rnd = Random(45829)
httpd = HTTPServer(('localhost', port), partial(NoddyHandler, db, str(rnd.randrange(1000000000))))
httpd.serve_forever()
