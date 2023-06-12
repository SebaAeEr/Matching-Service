from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Time,
    Float,
    Date,
    BLOB,
    FLOAT,
    DATETIME,
)
from sqlalchemy.orm import relationship

from database import Base


class Messages(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    rule_id = Column(Integer, ForeignKey("rules.id", ondelete="CASCADE"))
    date = Column(DATETIME)
    message = Column(String)

    rule = relationship("Rules", back_populates="messages")


class Rules(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True)
    listen_to = Column(String)
    message_type = Column(String)
    exclusiv = Column(Boolean)

    messages = relationship("Messages", cascade="all, delete", back_populates="rule")
