from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class PropertyRequest(Base):
    __tablename__ = "propertyRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String, nullable=False)
    propertyType = Column(String, nullable=False)
    numberOfrooms = Column(Integer)
    budgetRange = Column(String, nullable=False)
    maxBudget = Column(String, nullable=False)
    notes = Column(String)
    isPaid = Column(Boolean, nullable=False)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User")


class HotelRequest(Base):
    __tablename__ = "hotelRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    checkInDate = Column(String, nullable=False)
    checkOutDate = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    numberOfGuests = Column(Integer, nullable=False)
    numberOfRooms = Column(Integer, nullable=False)
    budgetPerRoom = Column(Integer, nullable=False)
    isPaid = Column(Boolean, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class MeetingRoomRequest(Base):
    __tablename__ = "meetingRoomRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    checkInDate = Column(String, nullable=False)
    checkOutDate = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    numberOfGuests = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    budgetPerDay = Column(Integer, nullable=False)
    numberOfDays = Column(Integer, nullable=False)
    isPaid = Column(Boolean, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class EventHallRequest(Base):
    __tablename__ = "eventHallRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    numberOfGuests = Column(Integer, nullable=False)
    budgetPerDay = Column(Integer, nullable=False)
    numberOfDays = Column(Integer, nullable=False)
    isPaid = Column(Boolean, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class OfficeSpaceRequest(Base):
    __tablename__ = "officeSpaceRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    checkInDate = Column(String, nullable=False)
    checkOutDate = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    numberOfWorkers = Column(Integer, nullable=False)
    numberOfWorkstations = Column(Integer, nullable=False)
    budgetPerDay = Column(Integer, nullable=False)
    numberOfDays = Column(Integer, nullable=False)
    isPaid = Column(Boolean, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class PropertyManagement(Base):
    __tablename__ = "propertyManagementRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class ShortletRequest(Base):
    __tablename__ = "shortletRequests"

    id = Column(Integer, primary_key=True, nullable=False)
    checkInDate = Column(String, nullable=False)
    checkOutDate = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    numberOfRooms = Column(Integer, nullable=False)
    budgetPerDay = Column(Integer, nullable=False)
    numberOfDays = Column(Integer, nullable=False)
    isPaid = Column(Boolean, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phoneNumber = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(String, nullable=False)
    contactMethod = Column(String, nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, nullable=False)
    serviceId = Column(Integer, nullable=False)
    userId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
