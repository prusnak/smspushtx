import binascii
import string

import requests

messages = {}


def process_msg(msg):

    try:

        # single message
        if "concat" not in msg:
            # push it
            pushtx(msg["text"])
            return

        # split message
        ref = "%s:%s" % (msg["msisdn"], msg["concat-ref"])
        idx = int(msg["concat-part"])
        cnt = int(msg["concat-total"])

        # not seen before
        if ref not in messages:
            messages[ref] = cnt * [None]

        # assign value
        messages[ref][idx - 1] = msg["text"]

        # are all value set?
        if None not in messages[ref]:
            # get joined message
            joined = "".join(messages[ref])
            del messages[ref]
            # and push it
            pushtx(joined)

        print("PROCESSED OK")

    except Exception as ex:

        print("PROCESS ERROR", ex)


def pushtx(data):

    print('PUSHING "%s"' % data)

    # is it hex format?
    if all(c in string.hexdigits for c in data):
        decoded = data
    else:
        # try base64 decode, then convert to hex
        try:
            decoded = binascii.hexlify(binascii.a2b_base64(data)).decode()
        except:
            decoded = None

    if not decoded:
        print("PUSH DECODE ERROR")
        return

    endpoints = [
        "https://btc-bitcore4.trezor.io/api/tx/send",
        "https://btc-bitcore5.trezor.io/api/tx/send",
        "https://insight.bitpay.com/api/tx/send",
        "https://blockexplorer.com/api/tx/send",
    ]

    for e in endpoints:
        try:
            r = requests.post(e, json={"rawtx": decoded}, timeout=1)
            if r.status_code == 200:
                print("PUSH OK", e)
            else:
                print("PUSH ERROR", r.status_code, e)
        except Exception as ex:
            print("PUSH FAILED", e, ex)
