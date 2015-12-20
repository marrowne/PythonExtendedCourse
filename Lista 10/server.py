from xmlrpc.server import SimpleXMLRPCServer
from db_sync import *

server = SimpleXMLRPCServer(("localhost", 8000))
print("Listening on port 8000...")
server.register_instance(Database())
server.serve_forever()
