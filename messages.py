import binascii
import re
import string

import requests


def push_tx(data):

    data = data.strip()

    print('PUSHING "%s"' % data)

    # is it hex format?
    if all(c in string.hexdigits for c in data):
        tx = data
    else:
        # try base64 decode, then convert to hex
        try:
            tx = binascii.hexlify(binascii.a2b_base64(data)).decode()
        except:
            tx = None

    if not tx:
        print("PUSH DECODE ERROR")
        return

    tx = tx.strip()

    endpoints = [
        "https://blockstream.info/api/tx",
        "https://mempool.space/api/tx",
    ]

    for e in endpoints:
        try:
            r = requests.post(e, data=tx, timeout=1)
            if r.status_code == 200:
                print("PUSH OK", e, r.text)
            else:
                print("PUSH ERROR", r.status_code, e)
        except Exception as ex:
            print("PUSH FAILED", e, ex)


messages = {}


def enqueue_msg(ref, part, total, text):
    global messages
    # not seen before
    if ref not in messages:
        messages[ref] = total * [None]
    # assign current value
    messages[ref][part - 1] = text.strip()
    # are all values set?
    if None not in messages[ref]:
        # get joined message
        joined = "".join(messages[ref])
        # remove from cache
        del messages[ref]
        # and push it
        push_tx(joined)


def process_msg(msg):
    print("RECEIVED", msg)

    try:
        # split message - indicated by the backend
        if "concat-ref" in msg:
            # split message
            ref = "%s:%s" % (msg["msisdn"], msg["concat-ref"])
            part, total = int(msg["concat-part"]), int(msg["concat-total"])
            enqueue_msg(ref, part, total, msg["text"])
            print("PROCESSED OK")
            return

        # split message - indicated by the message prefix (#/#)
        r = re.match(r"^\((\d+)/(\d+)\)(.*)$", msg["text"])
        if r:
            ref = "%s:%s" % (msg["msisdn"], "noref")
            part, total, text = int(r.group(1)), int(r.group(2)), r.group(3)
            enqueue_msg(ref, part, total, text)
            print("PROCESSED OK")
            return

        # single message
        push_tx(msg["text"])
        print("PROCESSED OK")

    except Exception as ex:
        print("PROCESS ERROR", ex)
