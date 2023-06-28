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
        f_msgs.append(schemas.MessageBase(**match.dict()))
        for rule in match.dict()["rules"]:
            f_rules.append(rule)
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
    fields = body[2:-1].split("=")
    counter = 1
    for key in fields[0::2]:
        print(key)
        print(fields[counter])
        d[key] = json.loads(urllib.parse.unquote(fields[counter]))
        counter += 2
    return d


# @matcher.on_event("startup")
# async def run_task():
#     listener = Listener(1)
#     listener.start()


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
def lex_dist():
    result = string_dist.match_lex_dist(rules, messages)
    print(result)
    clean_rules_msgs(result)
    return result
