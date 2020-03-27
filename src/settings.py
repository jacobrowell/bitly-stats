# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv


load_dotenv()

BITLY_TOKEN = os.getenv("BITLY_TOKEN", None)
FILTER_TAG = os.getenv("FILTER_TAG", None)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", None)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", None)
