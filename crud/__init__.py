from .admins import (
    get_admins,
    get_admin,
    create_admin,
    update_admin,
    delete_admin,
    get_admin_by_email,
    authenticate_admin,
)

from .apartments_sale import (
    get_apartments_sale,
    get_apartment_sale,
    create_apartment_sale,
    update_apartment_sale,
    delete_apartment_sale,
)

from .apartments_rent import (
    get_apartments_rent,
    get_apartment_rent,
    create_apartment_rent,
    update_apartment_rent,
    delete_apartment_rent,
)

from .apartment_parts import (
    get_apartment_parts,
    get_apartment_part,
    create_apartment_part,
    update_apartment_part,
    delete_apartment_part,
)

from .rental_contracts import (
    get_rental_contract,
    get_rental_contract_by_part,
    get_rental_contracts,
    create_rental_contract,
    update_rental_contract,
    delete_rental_contract,
    get_expiring_contracts,
)

from .notifications import (
    get_notifications,
    create_notification,
    update_notification,
)

from .aux import (
    get_admin_phone_for_whatsapp,
)



