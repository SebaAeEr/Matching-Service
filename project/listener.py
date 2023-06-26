import os
import time

from celery import Celery
from database import SessionLocal

from celery.schedules import crontab
import asyncio
import random
from rocketchat_async import RocketChat

import rc_handler

import whisper
import threading


class Listener(threading.Thread):
    rc = RocketChat()
    old_msg_id = ""
    model = None

    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.model = whisper.load_model("base.en")

    def handle_message(self, channel_id, sender_id, msg_id, thread_id, msg, qualifier):
        """Simply print the message that arrived."""
        if msg_id != self.old_msg_id:
            print(msg)
            if msg == "":
                rc_handler.handle_vmessage(msg_id, self.model)
            else:
                rc_handler.handle_message(msg)
            self.old_msg_id = msg_id

    async def listen(self, address, username, password):
        while True:
            try:
                await self.rc.start(address, username, password)

                # A possible workflow consists of two steps:
                #
                # 1. Set up the desired callbacks...
                for channel_id, channel_type in await self.rc.get_channels():
                    await self.rc.subscribe_to_channel_messages(
                        channel_id, self.handle_message
                    )
                # 2. ...and then simply wait for the registered events.
                await self.rc.run_forever()
            except (RocketChat.ConnectionClosed, RocketChat.ConnectCallFailed) as e:
                print(f"Connection failed: {e}. Waiting a few seconds...")
                await asyncio.sleep(random.uniform(4, 8))
                print("Reconnecting...")

    def run(self):
        asyncio.run(
            self.listen(
                "wss://" + os.environ["RC_SERVER_URL"] + "/websocket",
                os.environ["RC_NAME"],
                os.environ["RC_PASSWORD"],
            )
        )
