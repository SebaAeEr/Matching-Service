from typing import List, Optional, Tuple
from pydantic import BaseModel, validator
import datetime as dt


class RuleBase(BaseModel):
    listen_to: str
    callback: str
    deletion_mode: str


class Rule(RuleBase):
    id: str
    correlator_url: str


class MessageBase(BaseModel):
    id: str
    message: str


class MessageMatches(MessageBase):
    callback: str
