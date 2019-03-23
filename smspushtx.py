#!/usr/bin/env python3

from flask import Flask, request
from messages import process_msg

app = Flask(__name__)


@app.route("/smspushtx", methods=["POST"])
def smspushtx():
    j = request.get_json()
    print(j)
    process_msg(j)
    return "", 200
