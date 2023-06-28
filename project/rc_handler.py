from rocketchat_API.rocketchat import RocketChat
from requests import sessions
import crud
from database import SessionLocal
from rocketchat_API.rocketchat import RocketChat as rc_api
import datetime
import os


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
                os.getenv("RC_NAME", "ge49qag"),
                os.getenv("RC_PASSWORD", "!Tumonline!135"),
                server_url="https://" + os.getenv("RC_SERVER_URL", "chat.tum.de"),
                session=session,
            )
            rocket.chat_post_message(message, channel="CorrelatorTest").json()


def handle_vmessage(msg_id, model):
    with sessions.Session() as session:
        rocket = rc_api(
            os.getenv("RC_NAME", "ge49qag"),
            os.getenv("RC_PASSWORD", "!Tumonline!135"),
            server_url="https://" + os.getenv("RC_SERVER_URL", "chat.tum.de"),
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
            result = model.transcribe("currentVM.mp3")
            return result["text"]
            # message = crud.get_vmessage(result["text"], SessionLocal())
            # if message != None:
            #     rocket.chat_post_message(message, channel="CorrelatorTest").json()

            # rocket.call_api_post(
            #     "chat.delete",
            #     kwargs={"roomId": "LgmTbH5bjaxDkdtGF", "msgId": str(msg_id)},
            #     use_json=True,
            # )
            # r = sr.Recognizer()
            # try:
            #     with sr.AudioFile("currentVM.wav") as source:
            #         # listen for the data (load audio to memory)
            #         audio_data = r.record(source)
            #         # recognize (convert from speech to text)
            #         text = r.recognize_google(audio_data, language="en-GB")
            #         message = crud.get_vmessage(text, SessionLocal())
            #         if message != None:
            #             rocket.chat_post_message(
            #                 message, channel="CorrelatorTest"
            #             ).json()
            # except:
            #     rocket.chat_post_message(
            #         "Ich konnte dich nicht verstehen :(. Bitte wiederhole deine Anfrage!",
            #         channel="CorrelatorTest",
            #     ).json()


def ask_again(message):
    with sessions.Session() as session:
        rocket = rc_api(
            os.getenv("RC_NAME", "ge49qag"),
            os.getenv("RC_PASSWORD", "!Tumonline!135"),
            server_url="https://" + os.getenv("RC_SERVER_URL", "chat.tum.de"),
            session=session,
        )
        rocket.chat_post_message(
            'Did you mean: "' + message + '"?', channel="CorrelatorTest"
        ).json()


# with sessions.Session() as session:
#     rocket = rc_api(
#         "ge49qag",
#         "!Tumonline!135",
#         server_url="https://chat.tum.de",
#         session=session,
#     )
#     rocket.rooms_clean_history(
#         room_id="LgmTbH5bjaxDkdtGF",
#         latest=datetime.datetime.now(tz=datetime.timezone.utc)
#         .replace(tzinfo=None)
#         .isoformat(),
#         oldest="2023-06-06T00:00:00",
#     )
