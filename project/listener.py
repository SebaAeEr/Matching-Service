import os
import asyncio
import random
from rocketchat_async import RocketChat as asnc_rc

import whisper
import threading
import main
import requests
import json
from requests import sessions
from rocketchat_API.rocketchat import RocketChat as rc_api
import datetime
import os


class Listener(threading.Thread):
    """Listener connects to RC server and listens to all messages send."""

    rc = asnc_rc()
    usr_name = ""
    password = ""
    server_url = "chat.tum.de"

    def __init__(self, threadID):
        """Load model base.en."""

        threading.Thread.__init__(self)
        self.threadID = threadID
        self.model = whisper.load_model("base.en")
        self.old_msg_id = 0

    def handle_message(self, channel_id, sender_id, msg_id, thread_id, msg, qualifier):
        """Take message if it is a voicemessage transcribe it with transcribe_vmessage and send it with send_message to callback url."""

        if msg_id != self.old_msg_id:
            if msg == "":
                msg = self.transcribe_vmessage()
            print(msg)
            self.old_msg_id = msg_id
            self.send_messages(msg, msg_id)

    def transcribe_vmessage(self):
        """Take last voice message from channel, and transcribe it."""

        with sessions.Session() as session:
            rocket = rc_api(
                os.getenv("RC_NAME", self.usr_name),
                os.getenv("RC_PASSWORD", self.password),
                server_url="https://" + self.server_url,
                session=session,
            )
            files = rocket.channels_files(
                room_id="LgmTbH5bjaxDkdtGF", room_name="CorrelatorTest"
            )

            file = files.json()["files"][-1]
            now = datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None)
            diff = now - datetime.datetime.fromisoformat(file["uploadedAt"][0:-1])

            # if the voicemessage is older than 3 seconds something went wrong and we ignore it.
            if diff < datetime.timedelta(0, 3):
                urls = file["url"].replace("https://" + self.server_url, "").split("/")
                api_path = "/".join(urls[0:-1]) + "/"
                method = urls[-1]
                r = rocket.call_api_get(method, api_path)
                open("currentVM.mp3", "wb").write(r.content)
                result = self.model.transcribe("currentVM.mp3")
                return result["text"]

    def send_messages(self, msg: str, msg_id):
        """Send message to callback for messages."""

        print("url:" + main.callback_message)
        payload = json.dumps({"message": msg, "id": msg_id})
        headers = {"Content-Type": "application/json"}
        requests.request("PUT", main.callback_message, headers=headers, data=payload)

    async def listen(self, address, username, password):
        """Start to listen to specific RC server. If message arrives call handle_message."""

        while True:
            try:
                await self.rc.start(address, username, password)
                for channel_id, channel_type in await self.rc.get_channels():
                    await self.rc.subscribe_to_channel_messages(
                        channel_id, self.handle_message
                    )
                await self.rc.run_forever()
            except (asnc_rc.ConnectionClosed, asnc_rc.ConnectCallFailed) as e:
                print(f"Connection failed: {e}. Waiting a few seconds...")
                await asyncio.sleep(random.uniform(4, 8))
                print("Reconnecting...")

    def run(self):
        """Start to listen to specific RC-server."""

        asyncio.run(
            self.listen(
                "wss://" +  self.server_url + "/websocket",
                os.getenv("RC_NAME", self.usr_name),
                os.getenv("RC_PASSWORD", self.password),
            )
        )
