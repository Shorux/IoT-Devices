import logging

from aiomqtt import Client as MQTTClient
from config import HOST, PORT, USERNAME, PASSWORD, SSL_CONTEXT

class Client:
    def __init__(self):
        self.client = MQTTClient(
            hostname=HOST,
            port=PORT,
            username=USERNAME,
            password=PASSWORD,
            tls_context=SSL_CONTEXT
        )

    @staticmethod
    def _check_device_id(topic) -> bool:
        is_has = 'device_id' in topic
        if not is_has:
            logging.error('Topic require device id')
        return is_has