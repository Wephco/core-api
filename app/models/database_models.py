from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phoneNumber = Column(String)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class PropertyRequest(Base):
    __tablename__ = "propertyRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String, nullable=False)
    property = Column(String, nullable=False)
    bedroom = Column(Integer)
    budgetRange = Column(String, nullable=False)
    maxBudget = Column(String, nullable=False)
    notes = Column(String)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User")


class HotelRequest(Base):
    __tablename__ = "hotelRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    