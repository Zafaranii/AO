from .enums import (
    PartStatusEnum,
    AdminRoleEnum,
)

from .admin import (
    AdminBase,
    AdminCreate,
    AdminUpdate,
    AdminResponse,
    AdminLogin,
)

from .apartment_sale import (
    ApartmentSaleBase,
    ApartmentSaleCreate,
    ApartmentSaleUpdate,
    ApartmentSaleResponse,
)

from .apartment_rent import (
    ApartmentRentBase,
    ApartmentRentCreate,
    ApartmentRentUpdate,
    ApartmentRentResponse,
    ApartmentRentWithParts,
)

from .apartment_part import (
    ApartmentPartBase,
    ApartmentPartCreate,
    ApartmentPartUpdate,
    ApartmentPartResponse,
)

from .rental_contract import (
    RentalContractBase,
    RentalContractCreate,
    RentalContractUpdate,
    RentalContractResponse,
)


from .auth import (
    Token,
    TokenData,
    WhatsAppLinkResponse,
)
