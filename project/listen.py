import asyncio
import random
from rocketchat_async import RocketChat


def handle_message(channel_id, sender_id, msg_id, thread_id, msg, qualifier):
    """Simply print the message that arrived."""
    print(msg)


async def main(address, username, password):
    while True:
        try:
            rc = RocketChat()
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


# Side note: Don't forget to use the wss:// scheme when TLS is used.
asyncio.run(main("ws://localhost:3000/websocket", "username", "password"))
