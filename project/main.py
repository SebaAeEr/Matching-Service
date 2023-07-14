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
from pydantic import BaseModel
import urllib.parse
import re
import uuid


correlator = FastAPI(docs_url="/ad_doc", redoc_url="/ad_redoc")
models.Base.metadata.create_all(bind=engine)
subs = None
callback_message = ""
callback_rule = ""


if __name__ == "__main__":
    uvicorn.run(correlator, host="0.0.0.0", port=8000)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def url_to_dict(body):
    d = {}
    fields = re.split("=|&", body[2:-1])
    print(fields)
    counter = 1
    for key in fields[0::2]:
        if fields[counter] == "":
            fields[counter] = "%5B%5D"
        d[key] = json.loads(urllib.parse.unquote(fields[counter]))
        counter += 2
    return d


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
def add_feedback(rulebase: schemas.RuleBase):
    rule = schemas.Rule(
        **rulebase.dict(),
        correlator_url="http://localhost:8000/add/matching",
        id=str(uuid.uuid4())
    )
    payload = json.dumps(rule.dict())
    print(payload)
    headers = {"Content-Type": "application/json"}
    requests.request("PUT", callback_rule, headers=headers, data=payload)
    return


@correlator.post("/add/matching")
async def add_matching(request: Request):
    # print(await request.body())
    d = url_to_dict(str(await request.body()))
    print(d)
