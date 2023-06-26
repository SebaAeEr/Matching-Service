from fastapi import Body, FastAPI, Form, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from requests import sessions
from pprint import pprint
from rocketchat_API.rocketchat import RocketChat

import crud
import schemas
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import whisper
from listener import Listener


correlator = FastAPI(docs_url="/ad_doc", redoc_url="/ad_redoc")
models.Base.metadata.create_all(bind=engine)
subs = None

if __name__ == "__main__":
    uvicorn.run(correlator, host="127.0.0.1", port=8000)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@correlator.on_event("startup")
async def run_task():
    listener = Listener(1)
    listener.start()


# with sessions.Session() as session:
#     rocket = RocketChat(

#         "ge49qag",
#         "!Tumonline!135",
#         server_url="https://chat.tum.de",
#         session=session,
#     )
#     global subs
#     subs = rocket.subscriptions_get_one(room_id="LgmTbH5bjaxDkdtGF")
#     pprint(subs.json())
#     data = await subs.read(100)
#     pprint(data.decode())
# pprint(rocket.me().json())
# pprint(rocket.channels_list().json())
# pprint(
#     rocket.chat_post_message("Hello World!", channel="CorrelatorTest").json()
# )
# pprint(rocket.rooms_info(room_name="CorrelatorTest").json())
# pprint(rocket.channels_info(channel="CorrelatorTest").json())
# pprint(rocket.channels_history(room_id="LgmTbH5bjaxDkdtGF").json())


@correlator.post("/message/add")
def add_feedback(
    message: schemas.MessageBase,
    rule: schemas.RulesBase,
    db: Session = Depends(get_db),
):
    return crud.add_Message(message, rule, db)


@correlator.post("/subscription")
def add_feedback():
    task = start_listen.delay()
    print("task id:", task.id)
