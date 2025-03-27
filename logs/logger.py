import logging
from datetime import datetime

logs = logging.getLogger('devices')
logs.setLevel(logging.DEBUG)


class DeviceLog:
    def __init__(self, log: str = '', message: str = None, device_id: int = None):
        self.device_name = f'Аппарат {device_id}: ' if device_id else ''
        self.log = log
        if message:
            message = self._add(message)
            logging.info(message)

    def info(self, message: str) -> str:
        message = self._add(message)
        logging.info(message)
        return message

    def error(self, message: str) -> str:
        message = self._add(message)
        logging.error(message)
        return message

    def as_list(self) -> list[str]:
        return self.log.split('\n')

    def _add(self, message: str) -> str:
        message = f'{datetime.now().strftime("%d.%m.%Y, %H:%M:%S")}: {self.device_name}{message}'
        self.log += message + '\n'
        return message

    def __repr__(self):
        return self.log