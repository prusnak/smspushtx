import binascii
import re
import string

import requests

logger = None


def push_tx(data):
    data = data.strip()

    logger.info(f"PUSHING '{data}'")

    # is it hex format?
    if all(c in string.hexdigits for c in data):
        tx = data
    else:
        # try base64 decode, then convert to hex
        try:
            tx = binascii.hexlify(binascii.a2b_base64(data)).decode()
        except Exception:
            tx = None

    if not tx:
        logger.info("PUSH DECODE ERROR")
        return

    tx = tx.strip()

    endpoints = [
        "https://blockstream.info/api/tx",
        "https://mempool.space/api/tx",
    ]

    for e in endpoints:
        try:
            r = requests.post(e, data=tx, timeout=30)
            if r.status_code == 200:
                logger.info(f"PUSH OK {e} {r.text}")
            else:
                logger.info(f"PUSH ERROR {r.status_code} {e}")
        except Exception as ex:
            logger.info(f"PUSH FAILED {e} {ex}")


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


def process(msg):
    logger.info(f"RECEIVED {msg}")

    try:
        # split message - indicated by the backend
        if "concat-ref" in msg:
            # split message
            ref = "%s:%s" % (msg["msisdn"], msg["concat-ref"])
            part, total = int(msg["concat-part"]), int(msg["concat-total"])
            enqueue_msg(ref, part, total, msg["text"])
            logger.info("PROCESSED OK")
            return

        # split message - indicated by the message prefix (#/#)
        r = re.match(r"^\((\d+)/(\d+)\)(.*)$", msg["text"])
        if r:
            ref = "%s:%s" % (msg["msisdn"], "noref")
            part, total, text = int(r.group(1)), int(r.group(2)), r.group(3)
            enqueue_msg(ref, part, total, text)
            logger.info("PROCESSED OK")
            return

        # single message
        push_tx(msg["text"])
        logger.info("PROCESSED OK")

    except Exception as ex:
        logger.info(f"PROCESS ERROR {ex}")
