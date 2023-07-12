from fastapi import Body, FastAPI, Form, Request, Depends, Header, Response
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

import models
from database import SessionLocal, engine
from pydantic import BaseModel
import urllib.parse
import json
import string_dist
import schemas
import re
import chatgpt
from enum import Enum
import matcher as m


matcher = FastAPI(docs_url="/ad_doc", redoc_url="/ad_redoc")
models.Base.metadata.create_all(bind=engine)
subs = None
messages = []
rules = []


async def print_request(request):
    print(f"request header       : {dict(request.headers.items())}")
    print(f"request query params : {dict(request.query_params.items())}")
    try:
        print(f"request json         : {await request.json()}")
    except Exception as err:
        # could not parse json
        print(f"request body         : {await request.body()}")


def clean_rules_msgs(f_results):
    global rules, messages
    f_msgs = []
    f_rules = []
    for match in f_results:
        f_msgs.append(schemas.MessageBase(**match))
        for rule in match["rules"]:
            if rule["deletion_mode"] == "single":
                f_rules.append(schemas.Rule(**rule))
    rules = list(filter(lambda x: x not in f_rules, rules))
    messages = list(filter(lambda x: x not in f_msgs, messages))


if __name__ == "__main__":
    uvicorn.run(matcher, host="127.0.0.1", port=27182)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def url_to_dict(body):
    d = {}
    fields = re.split("=|&", body[2:-1])
    counter = 1
    for key in fields[0::2]:
        if fields[counter] == "":
            fields[counter] = "%5B%5D"
        print(key)
        print(fields[counter])
        d[key] = json.loads(urllib.parse.unquote(fields[counter]))
        counter += 2
    return d


@matcher.post("/add/message")
async def test(
    request: Request,
):
    global messages
    d = url_to_dict(str(await request.body()))
    msg = schemas.MessageBase(**d["message"])
    messages.append(msg)
    print(messages)
    return


@matcher.post("/add/rule")
async def test(
    request: Request,
):
    global rules
    d = url_to_dict(str(await request.body()))
    r = schemas.Rule(**d["rule"])
    rules.append(r)
    print(rules)
    return


@matcher.get("/run/lex_dist")
def lex_dist(response: Response, request: Request):
    global rules, messages
    response.headers["CPEE-CALLBACK"] = "true"
    callback = request.headers.get("Cpee-Callback")
    matcher = m.Matcher(1, callback, rules, messages, m.Matching_Methods.lex_dist)
    matcher.start()
    return


@matcher.get("/run/phone_dist")
def phone_dist(response: Response, request: Request):
    global rules, messages
    response.headers["CPEE-CALLBACK"] = "true"
    callback = request.headers.get("Cpee-Callback")
    matcher = m.Matcher(1, callback, rules, messages, m.Matching_Methods.phone_dist)
    matcher.start()
    return


@matcher.get("/run/embedding")
def embedding(response: Response, request: Request):
    global rules, messages
    response.headers["CPEE-CALLBACK"] = "true"
    callback = request.headers.get("Cpee-Callback")
    matcher = m.Matcher(1, callback, rules, messages, m.Matching_Methods.embedding)
    matcher.start()
    return


@matcher.get("/run/ask_chatgpt")
def ask_chatgpt(response: Response, request: Request):
    global rules, messages
    response.headers["CPEE-CALLBACK"] = "true"
    callback = request.headers.get("Cpee-Callback")
    matcher = m.Matcher(1, callback, rules, messages, m.Matching_Methods.ask_chatgpt)
    matcher.start()
    return


@matcher.post("/delete/matches")
async def delete_matches(request: Request):
    global messages, rules
    d = url_to_dict(str(await request.body()))
    print(d)
    for name in d:
        clean_rules_msgs(d[name])
    print("messages:" + str(messages))
    print("rules: " + str(rules))
    return