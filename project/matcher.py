import string_dist
import schemas
import chatgpt
from enum import Enum
import threading
import json
import requests


class Matching_Methods(Enum):
    lex_dist = 1
    phone_dist = 2
    embedding = 3
    ask_chatgpt = 4


class Matcher(threading.Thread):
    callback = ""
    rules = []
    messages = []
    matching_method = -1

    def __init__(
        self,
        threadID,
        callback,
        rules,
        messages,
        matching_method: Matching_Methods,
    ):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.callback = callback
        self.rules = rules
        self.messages = messages
        self.matching_method = matching_method

    def run(
        self,
        dist_threshold=0.8,
        found_count_threshold=0.7,
        lex_method: string_dist.Lex_Methods = string_dist.Lex_Methods.jaro_winkler,
        phone_method: string_dist.Phone_Methods = string_dist.Phone_Methods.nysiis,
        embedding_model="text-similarity-davinci-001",
        embedding_threshold=0.1,
        ask_chatpgt_model="gpt-3.5-turbo",
    ):
        result_list = []
        for rule in self.rules:
            found = False
            d = {}
            for msg in self.messages:
                rule_string = rule.listen_to.lower()
                mesg_string = msg.message.lower()
                if self.matching_method == Matching_Methods.lex_dist:
                    exact, match = string_dist.lex_dist(
                        rule_string,
                        mesg_string,
                        phone_dist=False,
                        dist_threshold=dist_threshold,
                        found_count_threshold=found_count_threshold,
                        lex_method=lex_method,
                        phone_method=phone_method,
                    )
                elif self.matching_method == Matching_Methods.phone_dist:
                    exact, match = string_dist.lex_dist(
                        rule_string,
                        mesg_string,
                        phone_dist=True,
                        dist_threshold=dist_threshold,
                        found_count_threshold=found_count_threshold,
                        lex_method=lex_method,
                        phone_method=phone_method,
                    )
                elif self.matching_method == Matching_Methods.embedding:
                    match = chatgpt.embedding_chatgpt(
                        rule_string, mesg_string, embedding_model, embedding_threshold
                    )
                elif self.matching_method == Matching_Methods.ask_chatgpt:
                    match = chatgpt.ask_chatgpt(
                        rule_string, mesg_string, ask_chatpgt_model
                    )
                if match:
                    if found:
                        d["messages"].append(msg.dict())
                    else:
                        d = rule.dict()
                        d["method"] = self.matching_method.name
                        d["messages"] = [msg.dict()]
                        found = True
            if d != {}:
                result_list.append(d)

        print(result_list)
        payload = json.dumps(result_list)
        print(payload)
        headers = {"Content-Type": "application/json"}
        requests.request("PUT", self.callback, headers=headers, data=payload)
        return
