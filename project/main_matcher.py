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


async def print_request(request):
    print(f"request header       : {dict(request.headers.items())}")
    print(f"request query params : {dict(request.query_params.items())}")
    try:
        print(f"request json         : {await request.json()}")
    except Exception as err:
        # could not parse json
        print(f"request body         : {await request.body()}")


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
        try:
            d[key] = json.loads(urllib.parse.unquote(fields[counter]))
        except:
            d[key] = fields[counter]
        counter += 2
    return d


@matcher.post("/run/matching")
async def run_matching(response: Response, request: Request):
    print_request(request)
    d = url_to_dict(str(await request.body()))
    messages = list(map(lambda x: schemas.MessageBase(**x), d["messages"]))
    rules = list(map(lambda x: schemas.Rule(**x), d["rules"]))
    response.headers["CPEE-CALLBACK"] = "true"
    callback = request.headers.get("Cpee-Callback")
    matcher = m.Matcher(1, callback, rules, messages, m.Matching_Methods[d["method"]])
    matcher.start()
    return
