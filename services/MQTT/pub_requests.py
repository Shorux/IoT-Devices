import logging
import sys
import asyncio

from .client import Client
from config import TOPICS

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Publisher(Client):
    async def command_to(self, device_id: int, message: str, topic: str = TOPICS.control_topic_pub):
        if not self._check_device_id(topic):
            return
        topic = topic.format(device_id=device_id)

        async with self.client:
            await self.client.publish(topic, message.encode())
            logging.info(f"Команда отправлена в {topic}: {message}")
