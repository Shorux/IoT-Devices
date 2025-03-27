import logging

from .client import Client

from utils.strings import _
from config import TOPICS


class Listener(Client):
    async def response(self, device_id, topic=TOPICS.response_sub):
        if not self._check_device_id(topic):
            return
        topic = topic.format(device_id=device_id)
        await self._subscribe(topic)

    async def new_device(self, topic=TOPICS.new_device_sub):
        await self._subscribe(topic)

    async def _subscribe(self, topic):
        async with self.client:
            await self.client.subscribe(topic)
            logging.info(_.subscription_approved.format(topic=topic))

            async for msg in self.client.messages:
                command = msg.payload.decode()
                logging.info(_.command_from_topic.format(topic=topic, command=command))