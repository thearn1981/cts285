from flask import Flask, request
from markupsafe import escape

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World!'