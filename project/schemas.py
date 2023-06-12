from typing import List, Optional, Tuple
from pydantic import BaseModel, validator
import datetime as dt


class MessageBase(BaseModel):
    message: str


class Messages(MessageBase):
    id: int
    date: dt.datetime
    rule_id: int

    class Config:
        orm_mode = True


class RulesBase(BaseModel):
    exclusiv: bool
    listen_to: str
    message_type: str


class Rules(MessageBase):
    id: int

    class Config:
        orm_mode = True
