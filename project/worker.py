import os
import time

from celery import Celery
from database import SessionLocal

from celery.schedules import crontab
import asyncio
import random
from rocketchat_async import RocketChat
import rc_handler


celery = Celery("worker")
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://localhost:6379"
)

celery.conf.timezone = "Europe/Amsterdam"

rc = RocketChat()
old_msg_id = ""


def handle_message(channel_id, sender_id, msg_id, thread_id, msg, qualifier):
    global rc, old_msg_id
    """Simply print the message that arrived."""
    if msg_id != old_msg_id:
        print(msg)
        print(channel_id)
        rc_handler.handle_message(msg)
        old_msg_id = msg_id


async def listen(address, username, password):
    global rc
    while True:
        try:
            await rc.start(address, username, password)

            # A possible workflow consists of two steps:
            #
            # 1. Set up the desired callbacks...
            for channel_id, channel_type in await rc.get_channels():
                await rc.subscribe_to_channel_messages(channel_id, handle_message)
            # 2. ...and then simply wait for the registered events.
            await rc.run_forever()
        except (RocketChat.ConnectionClosed, RocketChat.ConnectCallFailed) as e:
            print(f"Connection failed: {e}. Waiting a few seconds...")
            await asyncio.sleep(random.uniform(4, 8))
            print("Reconnecting...")


@celery.task(name="start_listen")
def start_listen():
    print("asdf")
    asyncio.run(listen("wss://chat.tum.de/websocket", "ge49qag", "!Tumonline!135"))
