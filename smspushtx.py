#!/usr/bin/env python3

import logging
import sys

from flask import Flask, request

import messages

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

app = Flask(__name__)
messages.logger = app.logger


@app.route("/smspushtx", methods=["POST"])
def smspushtx():
    json = request.get_json()
    messages.process(json)
    return "", 200
