import datetime as dt
from datetime import datetime, date
from sqlalchemy.orm import Session

import models
import schemas
from typing import List
from fuzzywuzzy import fuzz
from sqlalchemy import or_, and_, not_, literal


def add_Message(message: schemas.MessageBase, rule: schemas.RulesBase, db: Session):
    first = (
        db.query(models.Rules)
        .filter(
            models.Rules.listen_to == rule.listen_to,
            models.Rules.exclusiv == rule.exclusiv,
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
    rule = (
        db.query(models.Rules)
        .filter(
            or_(
                and_(models.Rules.exclusiv, models.Rules.listen_to == phrase),
                and_(
                    not_(models.Rules.exclusiv),
                    literal(phrase).contains(models.Rules.listen_to),
                ),
            ),
            or_(
                models.Rules.message_type == "Text", models.Rules.message_type == "All"
            ),
        )
        .first()
    )
    if rule == None:
        return None
    message = (
        db.query(models.Messages).filter(models.Messages.rule_id == rule.id).first()
    )
    if message == None:
        return None
    return message.message


def get_vmessage(phrase: str, db: Session):
    rules = (
        db.query(models.Rules)
        .filter(
            or_(
                models.Rules.message_type == "Voice", models.Rules.message_type == "All"
            ),
        )
        .all()
    )
    print("message: ", phrase)
    print(rules)

    found_rules = []

    for rule in rules:
        if rule.exclusiv:
            if fuzz.ratio(rule.listen_to.lower(), phrase.lower()) > 90:
                found_rules.append(rule)
        else:
            if fuzz.partial_ratio(rule.listen_to.lower(), phrase.lower()) > 90:
                found_rules.append(rule)
    print(found_rules)

    if len(found_rules) == 0:
        return None
    elif len(found_rules) > 1:
        message = "Multiple matches found. What did you mean: "
        for rule in found_rules:
            message += '\n"' + rule.message + '"'
        return message
    else:
        message = (
            db.query(models.Messages).filter(models.Messages.rule_id == rule.id).first()
        )
        if message == None:
            return None
        return message.message
