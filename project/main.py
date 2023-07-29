from fastapi import Body, FastAPI, Form, Request, Depends, Header, Response
import uvicorn

import schemas
from listener import Listener
import json
import requests
import urllib.parse
import re
import uuid


correlator = FastAPI(docs_url="/ad_doc", redoc_url="/ad_redoc")
subs = None
callback_message = ""
callback_rule = ""


if __name__ == "__main__":
    uvicorn.run(correlator, host="0.0.0.0", port=8000)


def url_to_dict(body):
    """Takes body of request from cpee and turns it in a dictionary."""

    d = {}
    fields = re.split("=|&", body[2:-1])
    counter = 1
    for key in fields[0::2]:
        # place empty brackets in value field if it is empty
        if fields[counter] == "":
            fields[counter] = "%5B%5D"
        d[key] = json.loads(urllib.parse.unquote(fields[counter]))
        counter += 2
    return d


@correlator.on_event("startup")
async def run_task():
    """Start listener-thread for RocketChat"""

    listener = Listener(1)
    listener.start()


@correlator.post("/listen/messages")
def liste_messages(response: Response, request: Request):
    """Overwrite callback url to send messages to."""

    response.headers["CPEE-CALLBACK"] = "true"
    global callback_message
    callback_message = request.headers.get("Cpee-Callback")
    print(callback_message)
    return


@correlator.post("/listen/rules")
def liste_rules(response: Response, request: Request):
    """Overwrite callback url to send rules to."""

    response.headers["CPEE-CALLBACK"] = "true"
    global callback_rule
    callback_rule = request.headers.get("Cpee-Callback")
    print(callback_rule)
    return


@correlator.post("/add/rule")
def add_rule(rulebase: schemas.RuleBase):
    """Add a rule by sending it to the callback for rules."""

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
    """Prints out matchings for debugging."""

    d = url_to_dict(str(await request.body()))
    print(d)
