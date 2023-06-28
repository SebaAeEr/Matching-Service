from typing import List, Optional, Tuple
from pydantic import BaseModel, validator
import datetime as dt


class Rule(BaseModel):
    listen_to: str
    exclusiv: bool
    message_type: str


class MessageBase(BaseModel):
    id: str
    message: str


class MessageMatches(MessageBase):
    rules: list
