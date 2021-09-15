# SMSPushTX

Simple PushTX server to push Bitcoin transactions via SMS (using Nexmo/Vonage).

You can use either base64 or hex encoded raw transactions.

More info: [https://rusnak.io/how-to-push-bitcoin-transactions-via-sms/](https://rusnak.io/how-to-push-bitcoin-transactions-via-sms/)

## Sending longer messages than 160 characters

Modern GSM phones can split longer messages into chunks of 160 characters automatically.
These will be correctly concatenated together on the server automatically.

If your phone can't do this automatically, you can still do this manually by prefixing each message
using the following scheme:

* "(1/2)" and "(2/2)" for 2 messages
* "(1/3)", "(2/3)" and "(3/3)" for 3 messages
* "(1/4)", "(2/4)", "(3/4)", and "(4/4)" for 4 messages
* etc.

The space after the closing bracket is not necessary.

## Instructions

* In Nexmo/Vonage Settings: set Default SMS Setting > HTTP Method to `POST-JSON`
* In Nexmo/Vonage Numbers: set SMS Inbound Webhook URL to `http://server:port/smspushtx`
