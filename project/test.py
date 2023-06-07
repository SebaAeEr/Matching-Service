import asyncio
import random
from rocketchat_async import RocketChat
import time


def handle_message(channel_id, sender_id, msg_id, thread_id, msg, qualifier):
    global rc, old_msg
    """Simply print the message that arrived."""
    # if msg != old_msg:
    print(msg_id)
    print(msg)
    print(channel_id)
    old_msg = msg


async def main(address, username, password):
    global rc
    while True:
        try:
            rc = RocketChat()
            await rc.start(address, username, password)

            # A possible workflow consists of two steps:
            #
            # 1. Set up the desired callbacks...

            await rc.subscribe_to_channel_messages("LgmTbH5bjaxDkdtGF", handle_message)
            time.sleep(3)
            # 2. ...and then simply wait for the registered events.
            await rc.run_forever()
        except (RocketChat.ConnectionClosed, RocketChat.ConnectCallFailed) as e:
            print(f"Connection failed: {e}. Waiting a few seconds...")
            await asyncio.sleep(random.uniform(4, 8))
            print("Reconnecting...")


# Side note: Don't forget to use the wss:// scheme when TLS is used.
old_msg = ""
rc = RocketChat()
asyncio.run(main("wss://chat.tum.de/websocket", "ge49qag", "!Tumonline!135"))
