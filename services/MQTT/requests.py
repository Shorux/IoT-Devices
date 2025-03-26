import sys
import asyncio

from aiomqtt import Client

from config import HOST, PORT, USERNAME, PASSWORD, SSL_CONTEXT, PUB_TOPIC, SUB_TOPIC


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class MQTTRequests:
    def __init__(self, device_id: int, pub_topic=PUB_TOPIC, sub_topic=SUB_TOPIC):
        self.pub_topic = pub_topic.format(device_id)
        self.sub_topic = sub_topic.format(device_id)
        self.broker = HOST
        self.port = PORT
        self.username = USERNAME
        self.password = PASSWORD
        self.ssl_context = SSL_CONTEXT
        self.client = Client(
            hostname=self.broker,
            port=self.port,
            username=self.username,
            password=self.password,
            tls_context=self.ssl_context
        )

    async def response(self):
        async with self.client:
            await self.client.subscribe(self.sub_topic)
            print(f"✅ Подписка на {self.sub_topic} выполнена")
            async for msg in self.client.messages:
                command = msg.payload.decode()
                if command.startswith('123'):
                    print('Есть ответ')
                else:
                    print('Нет ответа')


    async def publish(self, message):
        async with self.client:
            print(f'Отправляю комманду {message}')
            await self.client.publish(self.pub_topic, message.encode())
            await asyncio.sleep(1)

        print(f"✅ Команда отправлена в {self.pub_topic}: {message}")
