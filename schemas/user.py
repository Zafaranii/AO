"""Legacy compatibility module for schemas.

All schemas have been moved into dedicated files under the `schemas`
package. This module re-exports them to avoid breaking existing imports of
`schemas.user` across the codebase.
"""

from .enums import (
    ApartmentTypeEnum,
    PartStatusEnum,
    AdminRoleEnum,
    NotificationStatusEnum,
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

from .notification import (
    NotificationBase,
    NotificationCreate,
    NotificationUpdate,
    NotificationResponse,
)

from .auth import (
    Token,
    TokenData,
    WhatsAppLinkResponse,
)
