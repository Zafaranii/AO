"""Legacy compatibility module for models.

All enums and models have been moved into dedicated files under the `models`
package. This module re-exports them to avoid breaking existing imports of
`models.user` across the codebase.
"""

from .enums import ApartmentType, PartStatus, AdminRole, NotificationStatus
from .admin import Admin
from .apartment_sale import ApartmentSale
from .apartment_rent import ApartmentRent
from .apartment_part import ApartmentPart
from .rental_contract import RentalContract
from .notification import Notification
