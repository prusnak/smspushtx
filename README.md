# SMSPushTX

Simple PushTX server to push Bitcoin transactions via SMS (using Nexmo).

You can use either base64 or hex encoded raw transactions.

More info: [https://rusnak.io/how-to-push-bitcoin-transactions-via-sms/](https://rusnak.io/how-to-push-bitcoin-transactions-via-sms/)

## Instructions

* In Nexmo Settings: set Default SMS Setting > HTTP Method to `POST-JSON`
* In Nexmo Numbers: set SMS Inbound Webhook URL to `http://server:port/smspushtx`
