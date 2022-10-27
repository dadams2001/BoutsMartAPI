from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():

    hello = "hello from Flask!"

    response_body = {
        "statusMessage": "Success!",
        "flaskMessage": hello
    }

    return response_body
