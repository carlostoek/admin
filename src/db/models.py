from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, Boolean, DateTime
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    is_vip = Column(Boolean, default=False)
    vip_expiry = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)