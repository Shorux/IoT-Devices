import os
import logging
import ssl

from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(os.getenv('DEBUG', False))
DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')
DEVICE_NAME = os.getenv('DEVICE_NAME')

# Broker settings
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
PUB_TOPIC = os.getenv('PUB_TOPIC')
SUB_TOPIC = os.getenv('SUB_TOPIC')
SSL_CONTEXT = ssl.create_default_context()

if not BOT_TOKEN:
    logging.error("BOT_TOKEN is not defined neither in .env file nor in environment variables")
    quit()
