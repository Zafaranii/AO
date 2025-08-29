from enum import Enum


class ApartmentTypeEnum(str, Enum):
    rent = "rent"
    purchase = "purchase"


class PartStatusEnum(str, Enum):
    available = "available"
    rented = "rented"
    upcoming_end = "upcoming_end"


class AdminRoleEnum(str, Enum):
    super_admin = "super_admin"
    admin = "admin"


class NotificationStatusEnum(str, Enum):
    upcoming_end = "upcoming_end"
    unpaid_rent = "unpaid_rent"
