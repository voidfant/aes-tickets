from sqlalchemy import Column, Integer, String

from db.database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, nullable=False, unique=False, index=True)
    message_id = Column(String, nullable=False, unique=True, index=True)
