import argparse
import os
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

PORT = 8000

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # os assumes paths begining with '/' are absolute
            print self.path
            if self.path.startswith('/'):
                self.path = self.path[1:]
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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('port', nargs='?', type=int, default=PORT,
            help='port number')
    args = parser.parse_args()
    return args

def main():
    try:
        args = parse_args()
        httpd = HTTPServer(('', args.port), MyHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down the web server...'
        httpd.socket.close()

if __name__ == '__main__':
    main()