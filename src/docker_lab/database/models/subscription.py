

from sqlalchemy import Column, Integer, Enum, String

from .base import BaseModel
from enums import SubType, SubStatus


class SubscriptionModel(BaseModel):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(256), nullable=False)

    fullname = Column(String(256), nullable=False)
    phone = Column(String(32), nullable=False)
    sub_type = Column(Enum(SubType), nullable=False)
    sub_status = Column(Enum(SubStatus), nullable=False)
