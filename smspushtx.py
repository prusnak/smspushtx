#!/usr/bin/env python3

from flask import Flask, request
import messages

app = Flask(__name__)
messages.logger = app.logger


@app.route("/smspushtx", methods=["POST"])
def smspushtx():
    json = request.get_json()
    messages.process(json)
    return "", 200
