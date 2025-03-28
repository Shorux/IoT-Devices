import logging

from .client import Client

from utils.strings import _, TOPICS
from logs.logger import DeviceLog
from ..database.engine import async_session
from ..database.requests import Orders


class Listener(Client):
    async def response(self, device_id, topic=TOPICS.response_sub):
        if not self._check_device_id(topic):
            return

        topic = topic.format(device_id=device_id)
        async  for msg in self._subscribe(topic):
            command = msg.payload.decode().strip('-').strip('.')
            if command == "not_confirmed":
                logging.info(f'Попытка включения реле без оплаты')
                continue
            else:
                logging.info(_.command_from_topic.format(topic=topic, command=command))

            try:
                command, transaction_id = command.split(',')
                transaction_id = transaction_id.replace('ID:', '')
                async with async_session() as session:
                    order = await Orders(session).get(transaction_id)
                log = DeviceLog(log=order.log)

                if command.startswith("confirmed:"):
                    duration = command.split(":")[-1]
                    log.info(f'Аппарат подтвердил получение команды и разрешил запуск на {duration} секунд')
                elif command.startswith("confirmed"):
                    log.info(f'Аппарат подтвердил получение команды и разрешил запуск на 30 секунд')
                elif command.startswith("relay") and "on" in command:
                    parts = command.split("on")
                    relay_index, duration = parts[0].replace("relay", ""), parts[1]
                    log.info(f'Клиент запустил реле {relay_index} на {duration} секунд')
                elif command.startswith("relay") and "stop" in command:
                    relay_index = command.replace("relay", "").replace("stop", "")
                    log.info(f'Клиент остановил реле {relay_index}')
                elif command.startswith("relay") and "resumed" in command:
                    relay_index = command.replace("relay", "").replace("resumed", "")
                    log.info(f'Клиент продолжил использование реле {relay_index}')
                elif command.startswith("relay") and "off" in command:
                    relay_index = command.replace("relay", "").replace("off", "")
                    log.info(f'Реле {relay_index} успешно завершил работу')

                async with async_session() as session:
                    await Orders(session).update(transaction_id, log=str(log))
            except Exception as e:
                logging.error(str(e))

    async def new_device(self, topic=TOPICS.new_device_sub):
        async for msg in self._subscribe(topic):
            command = msg.payload.decode()
            logging.info(_.command_from_topic.format(topic=topic, command=command))

    async def _subscribe(self, topic):
        async with self.client:
            await self.client.subscribe(topic)
            logging.info(_.subscription_approved.format(topic=topic))

            async for msg in self.client.messages:
                yield msg