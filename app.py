from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

from routes import *

wsgi_app = app

if __name__ == "__main__":
    import os
    host = os.environ.get('HOST', '0.0.0.0')
    try:
        port = int(os.environ.get('PORT', '5555'))
    except ValueError:
        port = 5555
    app.run(host, port)
