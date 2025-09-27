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
    studio_rental = "studio_rental"
    apartment_sale = "apartment_sale"


class BathroomTypeEnum(enum.Enum):
    shared = "shared"
    private = "private"


class FurnishedEnum(enum.Enum):
    yes = "yes"
    no = "no"


class BalconyEnum(enum.Enum):
    yes = "yes"
    shared = "shared"
    no = "no"


class LocationEnum(enum.Enum):
    maadi = "maadi"
    mokkattam = "mokkattam"


class CustomerSourceEnum(enum.Enum):
    facebook = "facebook"
    instagram = "instagram"
    google = "google"
    referral = "referral"
    walk_in = "walk_in"
    other = "other"


