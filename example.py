import framework

def hello(server, match):
    return "Hello world from routed function land!!!!"

def user(server, match):
    return "This is %s's user page!" % match.group(1)

if __name__ == '__main__':
    framework.ROUTES['\Auser/([a-zA-Z0-9]+)\Z'] = ('example', 'user')
    framework.ROUTES['hello'] = ('example', 'hello')
    framework.run()