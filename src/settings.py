# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv


load_dotenv()

BITLY_TOKEN = os.getenv("BITLY_TOKEN", None)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", None)
