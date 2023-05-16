from enum import Enum


class Roles(str, Enum):
    admin = "admin"
    support = "support"
    staff = "staff"
    customer = "customer"
    agent = "agent"


class Services(str, Enum):
    propertyRequest = "propertyRequest"
    hotelRequest = "hotelRequest"
    propertyListing = "propertyListing"
