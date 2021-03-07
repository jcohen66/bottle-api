import bottle
from api import names

app = application = bottle.default_app()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # By default, uses Python's WSGI server which is only for dev purposes.
    bottle.run(host = '127.0.0.1', port = 8000)


