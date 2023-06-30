import logging
from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from db import models
from typing import Union

from typing import Union


def get_tickets(db: Session) -> list:
    result = [[x.Ticket.user_id, x.Ticket.message_id] for x in db.execute(select(models.Ticket))]
    return result


# def get_ticket_by_user_id(db: Session, user_id: int) -> list:
#     data = db.execute(select(models.Ticket)
#                       .where(models.Ticket.user_id == user_id)).one()
#     return [data.Ticket.user_id, data.Ticket.message_id]


def get_ticket_by_message_id(db: Session, message_id: str) -> list:
    # try:
    #     data = db.execute(select(models.Ticket)
    #                       .where(models.Ticket.message_id == message_id)).one()
    #     return [data.Ticket.user_id, data.Ticket.message_id]
    # except Exception as e:
    #     logging.log(logging.ERROR, e)
    #     return []
    data = db.execute(select(models.Ticket)
                      .where(models.Ticket.message_id == message_id))
    if data:
        data = data.one()
        return [data.Ticket.user_id, data.Ticket.message_id]
    else:
        return []


def create_ticket(db: Session, user_id: str, message_id: str) -> bool:
    try:
        db.add(models.Ticket(
            user_id=user_id,
            message_id=message_id
        ))
        db.commit()
        return True
    except Exception as e:
        logging.log(logging.ERROR, e)
        return False
