#!/usr/bin/env python3

from flask import Flask, request
import nexmo
import os

from messages import process_msg

KEY, SECRET = os.getenv('NEXMO_KEY'), os.getenv('NEXMO_SECRET')

client = nexmo.Client(key=KEY, secret=SECRET)

app = Flask(__name__)


@app.route('/smspushtx', methods=['POST'])
def smspushtx():
    j = request.get_json()
    print(j)
    process_msg(j)
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=13730)
