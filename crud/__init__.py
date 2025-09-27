from .admins import (
    get_admins,
    get_admin,
    create_admin,
    update_admin,
    delete_admin,
    get_admin_by_email,
    get_admin_by_phone,
    get_admin_by_username,
    authenticate_admin,
    verify_admin_password,
    update_admin_email,
    update_admin_password,
)

from .apartments_sale import (
    get_apartments_sale,
    get_apartment_sale,
    create_apartment_sale,
    update_apartment_sale,
    delete_apartment_sale,
    get_apartments_sale_by_admin,
)

from .apartments_rent import (
    get_apartments_rent,
    get_apartment_rent,
    create_apartment_rent,
    update_apartment_rent,
    delete_apartment_rent,
    get_apartments_rent_by_admin,
    get_apartments_with_parts_by_admin,
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
    get_rental_contracts_by_studio_ordered,
    create_rental_contract,
    update_rental_contract,
    delete_rental_contract,
    get_expiring_contracts,
)

from .aux import (
    get_admin_phone_for_whatsapp,
)



