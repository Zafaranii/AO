"""Legacy module: re-exported from split CRUD modules.

This file is kept for backward compatibility in case any third-party code
imports from crud.user. All logic now lives in dedicated modules and is
re-exported here via `crud.__init__`.
"""

from .admins import (
    get_admin,
    get_admin_by_email,
    get_admins,
    create_admin,
    update_admin,
    delete_admin,
    authenticate_admin,
)

from .apartments import (
    get_apartment,
    get_apartments,
    create_apartment,
    update_apartment,
    delete_apartment,
)

from .apartment_parts import (
    get_apartment_part,
    get_apartment_parts,
    create_apartment_part,
    update_apartment_part,
    delete_apartment_part,
)

from .notifications import (
    get_notifications,
    create_notification,
    update_notification,
)

from .purchase_requests import (
    get_purchase_requests,
    create_purchase_request,
    get_purchase_request,
)

from .aux import (
    get_expiring_contracts,
    get_admin_phone_for_whatsapp,
)
