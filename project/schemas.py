from typing import List, Optional, Tuple
from pydantic import BaseModel, validator
import datetime as dt


class Rule(BaseModel):
    listen_to: str
    callback: str
    id: str
    deletion_mode: str

class MessageBase(BaseModel):
    id: str
    message: str


class MessageMatches(MessageBase):
    rules: list
