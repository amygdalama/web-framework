import argparse
import os
import re
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.router = Router(self)
        self.router.add('hello', hello)
        self.router.add('\Auser/([a-zA-Z0-9]+)\Z', user)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        try:
            # os assumes paths begining with '/' are absolute
            if self.path.startswith('/'):
                self.path = self.path[1:]

            routing_info = self.router.route(self.path)
            if routing_info:
                func, match = routing_info
                func(self, match)
            else:
                if self.path == '' or os.path.isdir(self.path):
                    filename = os.path.join(self.path, 'index.html')
                else:
                    filename = self.path
                f = open(filename)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
        except IOError:
            self.send_error(404, 'File not found: %s' % filename)
        return

class Router(object):
    def __init__(self, server):
        self.routes = {}
        self.server = server

    def add(self, route, func):
        self.routes[route] = func

    def route(self, route):
        for pattern in self.routes:
            match = re.match(pattern, route)
            if match:
                return self.routes[pattern], match

def hello(server, match):
    server.send_response(200)
    server.send_header('Content-type', 'text/html')
    server.end_headers()
    server.wfile.write("Hello world from routed function land!!!!")

def user(server, match):
    server.send_response(200)
    server.send_header('Content-type', 'text/html')
    server.end_headers()
    server.wfile.write("This is %s's user page!" % match.group(1))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', nargs='?', type=int, default=PORT,
            help='port number')
    args = parser.parse_args()
    return args

def run():
    try:
        args = parse_args()
        httpd = HTTPServer(('', args.port), MyHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down the web server...'
        httpd.socket.close()

if __name__ == '__main__':
    run()