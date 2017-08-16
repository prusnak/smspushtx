#!/usr/bin/env python3

from flask import Flask, request

from messages import process_msg, endpoints

from sys import argv

app = Flask(__name__)


@app.route('/smspushtx', methods=['POST'])
def smspushtx():
    j = request.get_json()
    print(j)
    process_msg(j, coin)
    return '', 200


if __name__ == '__main__':

    coin = 'btc'
    if argv[1]:
        coin = argv[1]
    if coin in endpoints:
        app.run(host='0.0.0.0', port=13730)
    else:
        print('UNKNOWN COIN')
