import datetime as dt
from datetime import datetime, date
from sqlalchemy.orm import Session

import models
import schemas
from typing import List
from sqlalchemy import or_, and_, not_, literal
from tokenization import tokenize
from string_dist import lex_dist
from chatgpt import embedding_chatgpt, ask_chatgpt
from rc_handler import ask_again


# def add_Message(message: schemas.MessageBase, rule: schemas.Rule, db: Session):
#     first = (
#         db.query(models.Rules)
#         .filter(
#             models.Rules.listen_to == rule.listen_to,
#             models.Rules.exclusiv == rule.exclusiv,
#             models.Rules.message_type == rule.message_type,
#         )
#         .first()
#     )
#     rule_id = -1
#     if first == None:
#         r = models.Rules(**rule.dict())
#         db.add(r)
#         db.commit()
#         db.refresh(r)
#         rule_id = r.id
#     else:
#         rule_id = first.id

#     today = datetime.today()

#     first = db.query(models.Messages).filter(models.Messages.rule_id == rule_id).first()
#     if first == None:
#         m = models.Messages(**message.dict(), date=today, rule_id=rule_id)
#         db.add(m)
#         db.commit()
#         db.refresh(m)
#     else:
#         db.query(models.Messages).filter(models.Messages.id == first.id).update(
#             {
#                 models.Messages.message: message.message,
#                 models.Messages.date: today,
#             },
#             synchronize_session="fetch",
#         )
#         db.commit()
#         m = db.query(models.Messages).filter(models.Messages.id == first.id).first()
#         db.refresh(m)

#     return m


# def get_message(phrase: str, db: Session):
#     rule = (
#         db.query(models.Rules)
#         .filter(
#             or_(
#                 and_(models.Rules.exclusiv, models.Rules.listen_to == phrase),
#                 and_(
#                     not_(models.Rules.exclusiv),
#                     literal(phrase).contains(models.Rules.listen_to),
#                 ),
#             ),
#             or_(
#                 models.Rules.message_type == "Text", models.Rules.message_type == "All"
#             ),
#         )
#         .first()
#     )
#     if rule == None:
#         return None
#     message = (
#         db.query(models.Messages).filter(models.Messages.rule_id == rule.id).first()
#     )
#     if message == None:
#         return None
#     return message.message


# def get_vmessage(phrase: str, db: Session):
#     rules = (
#         db.query(models.Rules)
#         .filter(
#             or_(
#                 models.Rules.message_type == "Voice", models.Rules.message_type == "All"
#             ),
#         )
#         .all()
#     )
#     found_rules = match_msg_rule(phrase, rules)
#     print(map(lambda rule: rule.listen_to, found_rules))

#     if len(found_rules) == 0:
#         return None
#     elif len(found_rules) > 1:
#         message = "Multiple matches found. What did you mean: "
#         for rule in found_rules:
#             message += (
#                 '\n"'
#                 + (
#                     db.query(models.Messages)
#                     .filter(models.Messages.rule_id == rule.id)
#                     .first()
#                     .message
#                 )
#                 + '"'
#             )
#         return message
#     else:
#         message = find_message_for_rule(found_rules[0], db)
#         if message == None:
#             return None
#         return message.message


# def match_msg_rule(msg: str, rules):
#     str_white = tokenize(msg)
#     found_rules = []
#     for rule in rules:
#         exact_matches, res = lex_dist(str_white, rule.listen_to)
#         if res:
#             if not exact_matches:
#                 ask_again(rule.listen_to)
#             else:
#                 found_rules.append(rule)
#     if len(found_rules) == 0:
#         for rule in rules:
#             exact_matches, res = lex_dist(msg, rule.listen_to)
#             if res:
#                 if not exact_matches:
#                     ask_again(rule.listen_to)
#                 else:
#                     found_rules.append(rule)
#     # if len(found_rules) == 0:
#     #     for rule in rules:
#     #         if embedding_chatgpt(msg, rule.listen_to):
#     #             found_rules.append(rule)
#     # if len(found_rules) == 0:
#     #     for rule in rules:
#     #         if ask_chatgpt(msg, rule.listen_to):
#     #             found_rules.append(rule)

#     return found_rules


# def find_message_for_rule(rule, db: Session):
#     message = (
#         db.query(models.Messages).filter(models.Messages.rule_id == rule.id).first()
#     )
#     return message
