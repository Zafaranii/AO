import enum


class ApartmentTypeEnum(enum.Enum):
    rent = "rent"
    purchase = "purchase"


class PartStatusEnum(enum.Enum):
    available = "available"
    rented = "rented"
    upcoming_end = "upcoming_end"


class AdminRoleEnum(enum.Enum):
    super_admin = "super_admin"
    admin = "admin"


class NotificationStatusEnum(enum.Enum):
    upcoming_end = "upcoming_end"
    unpaid_rent = "unpaid_rent"


