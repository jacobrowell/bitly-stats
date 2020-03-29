# -*- coding: utf-8 -*-
import logging
import sys
from datetime import datetime
from collections import defaultdict, OrderedDict
from urllib.parse import urljoin, urlencode

import requests
from telebot import TeleBot

import settings


# Validate settings
if not all([settings.TELEGRAM_TOKEN, settings.BITLY_TOKEN]):
    logging.critical("API tokens missing")
    sys.exit(1)

if not settings.TELEGRAM_CHAT_ID:
    logging.critical("Telegram chat id missing")
    sys.exit(1)


def filter_by_tag(tagname):
    def check_item(item):
        return tagname in item["tags"] if tagname else True

    return check_item


def group_stats(stats):
    grouped = defaultdict(dict)

    for name, clicks in stats.items():
        _, group, source = name.split()
        grouped[group][source] = clicks

    for group in grouped:
        grouped[group] = OrderedDict(sorted(grouped[group].items()))

    return grouped


def format_stats(stats):
    today = datetime.now().strftime("%d-%m-%Y")
    formatted = [
        f"Переходы по ссылкам на ботов за {today}",
        ""
    ]
    for group, items in stats.items():
        formatted.append(f"*{group}*")
        for source, clicks in items.items():
            formatted.append(f"- {source}: {clicks}")

        formatted.append("")

    return "\n".join(formatted)


api_base = "https://api-ssl.bitly.com/v4"

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {settings.BITLY_TOKEN}"})

user_data = session.get(f"{api_base}/user").json()
group_guid = user_data["default_group_guid"]

url = f"{api_base}/groups/{group_guid}/bitlinks"
bitlinks_data = session.get(url).json()

links = list(filter(filter_by_tag(settings.FILTER_TAG),
                    bitlinks_data["links"]))
link_stats = {}

for link in links:
    bitlink = link["id"]
    query_params = urlencode({
        "unit": "day",
        "units": 1,
    })
    url = f"{api_base}/bitlinks/{bitlink}/clicks/summary?{query_params}"
    link_data = session.get(url).json()
    link_stats[link["title"]] = link_data["total_clicks"]

link_stats_grouped = group_stats(link_stats)
link_stats_formatted = format_stats(link_stats_grouped)

bot = TeleBot(settings.TELEGRAM_TOKEN)
bot.send_message(settings.TELEGRAM_CHAT_ID,
                 link_stats_formatted,
                 parse_mode="markdown")
