import datetime as dt
from datetime import datetime, date
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

import models
import schemas
from typing import List


def add_Message(message: schemas.MessageBase, rule: schemas.RulesBase, db: Session):
    first = (
        db.query(models.Rules)
        .filter(
            models.Rules.listen_to == rule.listen_to,
            models.Rules.medium == rule.medium,
            models.Rules.message_type == rule.message_type,
        )
        .first()
    )
    rule_id = -1
    if first == None:
        r = models.Rules(**rule.dict())
        db.add(r)
        db.commit()
        db.refresh(r)
        rule_id = r.id
    else:
        rule_id = first.id

    today = datetime.today()

    first = db.query(models.Messages).filter(models.Messages.rule_id == rule_id).first()
    if first == None:
        m = models.Messages(**message.dict(), date=today, rule_id=rule_id)
        db.add(m)
        db.commit()
        db.refresh(m)
    else:
        db.query(models.Messages).filter(models.Messages.id == first.id).update(
            {
                models.Messages.message: message.message,
                models.Messages.date: today,
            },
            synchronize_session="fetch",
        )
        db.commit()
        m = db.query(models.Messages).filter(models.Messages.id == first.id).first()
        db.refresh(m)

    return m


def get_message(phrase: str, db: Session):
    rule = db.query(models.Rules).filter(models.Rules.listen_to == phrase).first()
    if rule == None:
        return None
    message = (
        db.query(models.Messages).filter(models.Messages.rule_id == rule.id).first()
    )
    if message == None:
        return None
    return message.message
