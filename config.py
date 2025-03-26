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
HOST = '3dc6927eb43a444ebbac794961b9b974.s1.eu.hivemq.cloud'
PORT = 8883
USERNAME = 'hivemq.webclient.1742899651883'
PASSWORD = '2j3$<7SYRA&m!v9wLVfn'
SSL_CONTEXT = ssl.create_default_context()

if not BOT_TOKEN:
    logging.error("BOT_TOKEN is not defined neither in .env file nor in environment variables")
    quit()
