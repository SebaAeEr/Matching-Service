import asyncio
import random
from rocketchat_async import RocketChat as rc_async
import time
from rocketchat_API.rocketchat import RocketChat as rc_api
from requests import sessions
import datetime
import requests
import speech_recognition as sr
from pydub import AudioSegment


def handle_message(channel_id, sender_id, msg_id, thread_id, msg, qualifier):
    global rc, old_msg
    """Simply print the message that arrived."""
    # if msg != old_msg:
    print(msg_id)
    print(msg)
    print(channel_id)
    if msg == "":
        with sessions.Session() as session:
            rocket = rc_api(
                "ge49qag",
                "!Tumonline!135",
                server_url="https://chat.tum.de",
                session=session,
            )
            files = rocket.channels_files(
                room_id="LgmTbH5bjaxDkdtGF", room_name="CorrelatorTest"
            )
            file = files.json()["files"][-1]
            now = datetime.datetime.now(tz=datetime.timezone.utc).replace(tzinfo=None)
            diff = now - datetime.datetime.fromisoformat(file["uploadedAt"][0:-1])

            if diff < datetime.timedelta(0, 3):
                urls = file["url"].replace("https://chat.tum.de", "").split("/")
                api_path = "/".join(urls[0:-1]) + "/"
                method = urls[-1]
                r = rocket.call_api_get(method, api_path)
                open("currentVM.mp3", "wb").write(r.content)
                vm = AudioSegment.from_mp3("currentVM.mp3")
                vm.export("currentVM.wav", format="wav")
                r = sr.Recognizer()
                with sr.AudioFile("currentVM.wav") as source:
                    # listen for the data (load audio to memory)
                    audio_data = r.record(source)
                    # recognize (convert from speech to text)
                    text = r.recognize_google(audio_data, language="de-DE")
                    print(text)


async def main(address, username, password):
    global rc
    while True:
        try:
            rc = rc_async()
            await rc.start(address, username, password)

            # A possible workflow consists of two steps:
            #
            # 1. Set up the desired callbacks...

            await rc.subscribe_to_channel_messages("LgmTbH5bjaxDkdtGF", handle_message)
            time.sleep(3)
            # 2. ...and then simply wait for the registered events.
            await rc.run_forever()
        except (rc_async.ConnectionClosed, rc_async.ConnectCallFailed) as e:
            print(f"Connection failed: {e}. Waiting a few seconds...")
            await asyncio.sleep(random.uniform(4, 8))
            print("Reconnecting...")


# Side note: Don't forget to use the wss:// scheme when TLS is used.
old_msg = ""
rc = rc_async()
asyncio.run(main("wss://chat.tum.de/websocket", "ge49qag", "!Tumonline!135"))
