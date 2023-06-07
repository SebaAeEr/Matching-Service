from rocketchat_API.rocketchat import RocketChat
from requests import sessions
import crud
from database import SessionLocal
import schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def handle_message(chat: str):
    with SessionLocal() as session:
        message = crud.get_message(chat, session)
    if message != None:
        with sessions.Session() as session:
            rocket = RocketChat(
                "ge49qag",
                "!Tumonline!135",
                server_url="https://chat.tum.de",
                session=session,
            )
            subs = rocket.chat_post_message(message, channel="CorrelatorTest").json()
