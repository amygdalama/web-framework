from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write("Hello World!")
        return

def main():
    try:
        PORT = 8000
        httpd = HTTPServer(('', PORT), MyHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print 'Shutting down the web server...'
        httpd.socket.close()

if __name__ == '__main__':
    main()