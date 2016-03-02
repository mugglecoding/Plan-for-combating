__author__ = 'Arnout Aertgeerts'

import sys
if sys.version_info.major == 3:
    import http.server as SimpleHTTPServer
    import socketserver as SocketServer
else:
    import SimpleHTTPServer
    import SocketServer
import os
import json

class ChartRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def __init__(self, request, client_address, server):
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)
        return

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        body = json.loads(self.rfile.read(content_len))

        if 'options' in body:
            with open(body['name'], 'w') as json_file:
                json_file.write(json.dumps(body['options']))
        else:
            with open(body['name'], 'w') as chart_file:
                chart_file.write(body['svg'])

        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def log_message(self, format, *args):
        pass


class ChartServer(SocketServer.TCPServer):

    def __init__(self, server_address, handler_class=ChartRequestHandler):
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return


def run_server():
    import threading

    address = ('localhost', 0)  # let the kernel give us a port
    server = ChartServer(address, ChartRequestHandler)
    ip, port = server.server_address  # find out what port we were given

    print('Server running in the folder {0} at {1}:{2}'.format(os.path.abspath(os.getcwd()), ip, port))

    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True)  # don't hang on exit
    t.start()

    return 'http://{0}:{1}/'.format(ip, port)


address = run_server()


def url(path):
    return address + path