from enum import Enum


class PartStatusEnum(str, Enum):
    available = "available"
    rented = "rented"
    upcoming_end = "upcoming_end"


class AdminRoleEnum(str, Enum):
    super_admin = "super_admin"
    studio_rental = "studio_rental"
    apartment_sale = "apartment_sale"


class BathroomTypeEnum(str, Enum):
    shared = "shared"
    private = "private"


class FurnishedEnum(str, Enum):
    yes = "yes"
    no = "no"


class BalconyEnum(str, Enum):
    yes = "yes"
    shared = "shared"
    no = "no"


class LocationEnum(str, Enum):
    maadi = "maadi"
    mokkattam = "mokkattam"


class CustomerSourceEnum(str, Enum):
    facebook = "facebook"
    instagram = "instagram"
    google = "google"
    referral = "referral"
    walk_in = "walk_in"
    other = "other"
