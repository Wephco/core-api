from enum import Enum


class Roles(str, Enum):
    admin = "admin"
    support = "support"
    staff = "staff"
    customer = "customer"
    agent = "agent"
    super_admin = "super_admin"


class Services(str, Enum):
    propertyRequest = "propertyRequest"
    hotelRequest = "hotelRequest"
    propertyListing = "propertyListing"


class PropertyTypes(str, Enum):
    flat = "flat"
    bungalow = "bungalow"
    duplex = "duplex"
    mansion = "mansion"
    self_contain = "self_contain"
    mini_flat = "mini_flat"
    land = "land"
    office_space = "office_space"
    warehouse = "warehouse"
    shop = "shop"
    hotel = "hotel"
    guest_house = "guest_house"
    event_center = "event_center"
    hall = "hall"
    conference_center = "conference_center"
    restaurant = "restaurant"
    bar = "bar"
    lounge = "lounge"
    night_club = "night_club"
    hostel = "hostel"
    short_let = "short_let"
    house = "house"
    room = "room"
    other = "other"


class AuthorizationCodes(str, Enum):
    wephco_admin = "wephco_admin"
    wephco_ceo = "OZIOMA2022"
    super_admin = "neto"
