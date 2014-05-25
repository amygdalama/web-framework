import server

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

if __name__ == '__main__':
    server.ROUTES['\Auser/([a-zA-Z0-9]+)\Z'] = ('example', 'user')
    server.ROUTES['hello'] = ('example', 'hello')
    server.run()