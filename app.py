from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

from routes import *

wsgi_app = app

if __name__ == "__main__":
    import os
    host = os.environ.get('SERVER_HOST', 'localhost')
    try:
        port = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        port = 5555
    app.run(host, port)