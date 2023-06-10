from rocketchat_API.rocketchat import RocketChat
from requests import sessions
import crud
from database import SessionLocal
import schemas
from rocketchat_API.rocketchat import RocketChat as rc_api
import datetime
import speech_recognition as sr
from pydub import AudioSegment


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
            rocket.chat_post_message(message, channel="CorrelatorTest").json()


def handle_vmessage():
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
            try:
                with sr.AudioFile("currentVM.wav") as source:
                    # listen for the data (load audio to memory)
                    audio_data = r.record(source)
                    # recognize (convert from speech to text)
                    text = r.recognize_google(audio_data, language="de-DE")
                    handle_message(text)
            except:
                rocket.chat_post_message(
                    "Ich konnte dich nicht verstehen :(. Bitte wiederhole deine Anfrage!",
                    channel="CorrelatorTest",
                ).json()
