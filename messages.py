messages = {}


def process_msg(msg):

    try:

        # single message
        if 'concat' not in msg:
            # push it
            pushtx(msg['text'])
            return

        # split message
        ref = '%s:%s' % (msg['msisdn'], msg['concat-ref'])
        idx = int(msg['concat-part'])
        cnt = int(msg['concat-total'])

        # not seen before
        if ref not in messages:
            messages[ref] = cnt * [None]

        # assign value
        messages[ref][idx - 1] = msg['text']

        # are all value set?
        if None not in messages[ref]:
            # get joined message
            joined = ''.join(messages[ref])
            del messages[ref]
            # and push it
            pushtx(joined)

        print('PROCESSED OK')

    except Exception as ex:

        print('PROCESS ERROR', ex)


def pushtx(data):
    print('PUSHING "%s"' % data)
    # TODO
