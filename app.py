from flask import Flask, jsonify
app = Flask(__name__)

app.config["USERNAME"] = "onego"
app.config["PASSWORD"] = "test123"
app.config["HOST"] = "onegodev.ddns.net"
app.config["PORT"] = "2727"
app.config["DATABASE"] = "onego"



@app.route('/')
def hello():
    return "Hello world!"
