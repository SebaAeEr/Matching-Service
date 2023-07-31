from typing import List, Optional, Tuple
from pydantic import BaseModel, validator
import datetime as dt


class RuleBase(BaseModel):
    listen_to: str
    callback: str


class Rule(RuleBase):
    id: str


class MessageBase(BaseModel):
    id: str
    message: str


class Matches(BaseModel):
    message: str
    callback: str
