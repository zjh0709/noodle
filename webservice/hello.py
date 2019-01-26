from flask import Flask
from flask import g

app = Flask(__name__)


@app.route("/")
def hello_world():
    g.hello = "hello world!"
    return g.hello


@app.route("/hey")
def hey_world():
    return g.hello


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
