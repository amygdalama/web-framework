import argparse
import os
import re
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT = 8000
ROUTES = {}

class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.router = Router(self)
        for key, value in ROUTES.items():
            self.router.add(key, value)
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        try:
            # os assumes paths begining with '/' are absolute
            if self.path.startswith('/'):
                self.path = self.path[1:]

            routing_info = self.router.route(self.path)
            if routing_info:
                func_info, regex_match = routing_info
                module_name, func_name = func_info
                module = __import__(module_name)
                func = getattr(module, func_name)
                content = func(self, regex_match)
            else:
                if self.path == '' or os.path.isdir(self.path):
                    filename = os.path.join(self.path, 'index.html')
                else:
                    filename = self.path
                f = open(filename)
                content = f.read()
                f.close()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        except IOError:
            self.send_error(404, 'File not found: %s' % filename)
        return

class Router(object):
    def __init__(self, server):
        self.routes = {}
        self.server = server

    def add(self, route, value):
        self.routes[route] = value

    def route(self, route):
        for pattern in self.routes:
            match = re.match(pattern, route)
            if match:
                return self.routes[pattern], match

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