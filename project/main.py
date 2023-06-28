from fastapi import Body, FastAPI, Form, Request, Depends, Header, Response
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
from listener import Listener
import json
import requests


correlator = FastAPI(docs_url="/ad_doc", redoc_url="/ad_redoc")
models.Base.metadata.create_all(bind=engine)
subs = None
callback_message = ""
callback_rule = ""


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


@correlator.post("/listen/messages")
def test(response: Response, request: Request):
    response.headers["CPEE-CALLBACK"] = "true"
    global callback_message
    callback_message = request.headers.get("Cpee-Callback")
    print(callback_message)
    return


@correlator.post("/listen/rules")
def test(response: Response, request: Request):
    response.headers["CPEE-CALLBACK"] = "true"
    global callback_rule
    callback_rule = request.headers.get("Cpee-Callback")
    print(callback_rule)
    return


@correlator.post("/add/rule")
def add_feedback(
    message: schemas.MessageBase,
    rule: schemas.Rule,
    db: Session = Depends(get_db),
):
    print(callback_rule)
    payload = json.dumps(rule.dict())
    print(payload)
    headers = {"Content-Type": "application/json"}
    requests.request("PUT", callback_rule, headers=headers, data=payload)
    return


# return crud.add_Message(message, rule, db)
