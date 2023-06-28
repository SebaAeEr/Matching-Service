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
import main
import requests
import json


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
            if msg == "":
                msg = rc_handler.handle_vmessage(msg_id, self.model)
            print(msg)
            self.old_msg_id = msg_id
            self.send_messages(msg, msg_id)

    def send_messages(self, msg: str, msg_id):
        print("url:" + main.callback_message)
        payload = json.dumps({"message": msg, "id": msg_id})
        headers = {"Content-Type": "application/json"}
        requests.request("PUT", main.callback_message, headers=headers, data=payload)

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
                "wss://" + os.getenv("RC_SERVER_URL", "chat.tum.de") + "/websocket",
                os.getenv("RC_NAME", "ge49qag"),
                os.getenv("RC_PASSWORD", "!Tumonline!135"),
            )
        )
