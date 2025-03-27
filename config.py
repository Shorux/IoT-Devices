import os
import logging
import ssl

from dotenv import load_dotenv

load_dotenv()

DEBUG = bool(int(os.getenv('DEBUG', 0)))
DATABASE_URL = os.getenv('DATABASE_URL')
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Broker settings
HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
SSL_CONTEXT = ssl.create_default_context()

DEVICES = [1, 2]

class TOPICS:
    # subscription topics
    response_sub = 'devices/{device_id}/response'
    new_device_sub = 'devices/new_device'

    # publish topics
    control_topic_pub = 'devices/{device_id}/control'

if not BOT_TOKEN:
    logging.error("BOT_TOKEN is not defined neither in .env file nor in environment variables")
    quit()
