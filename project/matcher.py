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
    """Matcher thread offering different matching methods."""

    def __init__(
        self,
        threadID,
        callback,
        rules,
        messages,
        matching_method: Matching_Methods,
    ):
        """
        callback: callback url matches will be send to
        rules: rules for matching
        messages: messages for matching
        matching_method: method used for matching, Enum Matching_Methods
        """

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
        """
        Run the matching method with
        dist_threshold: threshold for the distance between two words (only for lex_dist and phone_dist)
        found_count_threshold: threshold on percentage for how many words in string rule.listen_to where matched to message
        lex_method: method used by lex_dist
        phone_method: method used by phone_dist
        embedding_model: model for embedding
        embedding_threshold: threshold for embedding
        ask_chatgpt_model: model of chatgpt
        """
        result_list = []
        for rule in self.rules:
            # match lower case message and rule
            rule_string = rule.listen_to.lower()
            for msg in self.messages:
                msg_string = msg.message.lower()
                if self.matching_method == Matching_Methods.lex_dist:
                    match = string_dist.lex_dist(
                        rule_string,
                        msg_string,
                        phone_dist=False,
                        dist_threshold=dist_threshold,
                        found_count_threshold=found_count_threshold,
                        lex_method=lex_method,
                        phone_method=phone_method,
                    )
                elif self.matching_method == Matching_Methods.phone_dist:
                    match = string_dist.lex_dist(
                        rule_string,
                        msg_string,
                        phone_dist=True,
                        dist_threshold=dist_threshold,
                        found_count_threshold=found_count_threshold,
                        lex_method=lex_method,
                        phone_method=phone_method,
                    )
                elif self.matching_method == Matching_Methods.embedding:
                    match = chatgpt.embedding_chatgpt(
                        rule_string, msg_string, embedding_model, embedding_threshold
                    )
                elif self.matching_method == Matching_Methods.ask_chatgpt:
                    match = chatgpt.ask_chatgpt(
                        rule_string, msg_string, ask_chatpgt_model
                    )
                if match:
                    result_list.append(
                        {
                            "callback": rule.callback,
                            "message": msg.message,
                            "rule_id": rule.id,
                            "msg_id": msg.id,
                        }
                    )
                    # continue with next rule after first match => first match always wins
                    break

        # send result as JSON back to callback
        payload = json.dumps(result_list)
        print(payload)
        headers = {"Content-Type": "application/json"}
        requests.request("PUT", self.callback, headers=headers, data=payload)
        return
