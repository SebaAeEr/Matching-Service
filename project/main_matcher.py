from fastapi import Body, FastAPI, Form, Request, Depends, Header, Response
import uvicorn
import urllib.parse
import json
import schemas
import re
import matcher as m


matcher = FastAPI(docs_url="/ad_doc", redoc_url="/ad_redoc")
thread_counter = 0


async def print_request(request):
    """Print full requests for debugging"""

    print(f"request header       : {dict(request.headers.items())}")
    print(f"request query params : {dict(request.query_params.items())}")
    try:
        print(f"request json         : {await request.json()}")
    except Exception as err:
        # could not parse json
        print(f"request body         : {await request.body()}")


if __name__ == "__main__":
    uvicorn.run(matcher, host="127.0.0.1", port=27182)


def url_to_dict(body):
    """Takes body of request from cpee and turns it in a dictionary."""

    d = {}
    fields = re.split("=|&", body[2:-1])
    counter = 1
    for key in fields[0::2]:
        # place empty brackets in value field if it is empty
        if fields[counter] == "":
            fields[counter] = "%5B%5D"
        try:
            d[key] = json.loads(urllib.parse.unquote(fields[counter]))
        except:
            d[key] = fields[counter]
        counter += 2
    return d


@matcher.post("/run/matching")
async def run_matching(response: Response, request: Request):
    """
    Create thread to run the specific matching method with request body:
    messages: []
    rules: []
    method: str
    """

    global thread_counter
    d = url_to_dict(str(await request.body()))
    messages = list(map(lambda x: schemas.MessageBase(**x), d["messages"]))
    rules = list(map(lambda x: schemas.Rule(**x), d["rules"]))
    response.headers["CPEE-CALLBACK"] = "true"
    callback = request.headers.get("Cpee-Callback")
    matcher = m.Matcher(
        thread_counter, callback, rules, messages, m.Matching_Methods[d["method"]]
    )
    thread_counter += 1
    matcher.start()
    return
