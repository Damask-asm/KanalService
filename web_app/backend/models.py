# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Order(Base):
    __tablename__ = 'orders'

    ordernumber = Column(Integer, primary_key=True, server_default=text("nextval('orders_ordernumber_seq'::regclass)"))
    costdollar = Column(Float(53), nullable=False)
    costruble = Column(Float(53), nullable=False)
    deliverytime = Column(DateTime, nullable=False)
