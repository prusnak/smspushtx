#!/usr/bin/env python3

from flask import Flask, request
from messages import process_msg

app = Flask(__name__)


@app.route("/smspushtx", methods=["POST"])
def smspushtx():
    json = request.get_json()
    process_msg(json)
    return "", 200
