# API Changes: Location (free text) and Customer source (new values)

This document records **all API- and data-layer changes** introduced in the same work session as: free-form `location` on apartment endpoints, the apartment sale `PUT` handler fix, and extended `how_did_customer_find_us` (customer source) values on rental contract endpoints. It is written in the same spirit as `TESTING.md`, `FRONTEND_INTEGRATION_GUIDE.md`, and `API_DOCUMENTATION.md`—endpoint-focused, with request fields and examples.

**Base URL:** `http://localhost:8000/api/v1`  
**Authentication (where required):** `Authorization: Bearer <your_jwt_token>`  
**Content-Type:** `application/json` (unless noted)

---

## 1. `location` field — apartments (sale and rent)

### 1.1 Summary of change

| Aspect | Before | After |
|--------|--------|--------|
| Pydantic / OpenAPI | `location` was restricted to a small enum (e.g. `maadi`, `mokkattam`) | `location` is a **string**; **any** non-empty free text is accepted |
| SQLAlchemy models | `location` was `Enum(LocationEnum)` | `location` is `String(255)` |
| `LocationEnum` | Present in `models/enums.py` and `schemas/enums.py` | **Removed** (no longer used) |

**Important:** Existing MySQL tables that were created with an enum for `location` must be **altered** to `VARCHAR(255)` (or equivalent) for arbitrary strings to persist. If the column remains an old enum, inserts/updates with new values can fail with MySQL `Data truncated for column 'location'`.

### 1.2 Affected API endpoints

All requests and responses that include apartment `name` and `location` for **sale** and **rent** are affected.

| Method | Path | Change |
|--------|------|--------|
| `POST` | `/apartments/sale` | Request body: `location` is free string |
| `PUT` | `/apartments/sale/{apartment_id}` | Request body: optional `location` is free string |
| `GET` | `/apartments/sale` | Response items: `location` is string |
| `GET` | `/apartments/sale/{apartment_id}` | Response: `location` is string |
| `POST` | `/apartments/rent` | Request body: `location` is free string |
| `PUT` | `/apartments/rent/{apartment_id}` | Request body: optional `location` is free string |
| `GET` | `/apartments/rent` | Response items: `location` is string |
| `GET` | `/apartments/rent/{apartment_id}` | Response: `location` is string |
| `GET` | `/apartments/my-content` | Nested sale/rent content: `location` is string |

**Related (read-only, echoes apartment data):**  
- `GET /apartments/rent/{apartment_id}/whatsapp` — the generated message includes `apartment.name` and `apartment.location` as plain text; `location` can now be any string the listing uses.

### 1.3 Example: create apartment for sale (custom location)

**POST** `/apartments/sale`

```json
{
  "name": "Tower View",
  "location": "Fifth Settlement Block 9",
  "address": "Street 1",
  "area": 120.5,
  "number": "A-201",
  "price": 2500000,
  "bedrooms": 3,
  "bathrooms": "private",
  "description": "Spacious unit",
  "photos_url": ["https://example.com/1.jpg"]
}
```

### 1.4 Example: update only location (apartment sale)

**PUT** `/apartments/sale/123`

```json
{
  "location": "Nasr City - Zone 5"
}
```

### 1.5 Bug fix: `PUT /apartments/sale/{id}`

A naming collision in the router caused `PUT` sale updates to call the wrong function and return **500**. The route handler was renamed and the CRUD `update` function was **imported under an alias** so `PUT /apartments/sale/{apartment_id}` works correctly. Behavior from the client’s perspective: **same URL and body schema**; the endpoint no longer errors for that reason.

### 1.6 Sample data / setup script

- `setup.py` sample data now passes **string** literals for `location` (e.g. `"maadi"`, `"mokkattam"`) instead of `LocationEnum` members.

---

## 2. `how_did_customer_find_us` (customer source) — rental contracts

### 2.1 Summary of change

| Aspect | Change |
|--------|--------|
| Enum (Python) | `CustomerSourceEnum` in `models/enums.py` and `schemas/enums.py` now includes: **`Bayut`**, **`Aqar map`**, **`Dubizzle`** (in addition to `facebook`, `instagram`, `google`, `referral`, `walk_in`, `other`) |
| MySQL | Column `rental_contracts.how_did_customer_find_us` enum definition was extended to include the same new labels **if** you run the migration (see below) |
| ORM | `RentalContract.how_did_customer_find_us` uses SQLAlchemy `Enum` with **`values_callable` set to member values** so stored strings like `"Aqar map"` (with a space) round-trip correctly on read/refresh |

**API string values to send (exact, case- and space-sensitive in JSON):**

- `"facebook"`, `"instagram"`, `"google"`
- `"Bayut"`, `"Aqar map"`, `"Dubizzle"`
- `"referral"`, `"walk_in"`, `"other"`

### 2.2 Affected API endpoints

| Method | Path | Field |
|--------|------|--------|
| `POST` | `/rental-contracts/` | `how_did_customer_find_us` |
| `PUT` | `/rental-contracts/{contract_id}` | optional `how_did_customer_find_us` |
| `GET` | `/rental-contracts/` (and related list/detail) | `how_did_customer_find_us` in responses |

### 2.3 Example: create rental contract (new source)

**POST** `/rental-contracts/`

```json
{
  "apartment_part_id": 1,
  "customer_name": "Test Customer",
  "customer_phone": "+201234567890",
  "customer_id_number": "12345678901234",
  "how_did_customer_find_us": "Bayut",
  "paid_deposit": 5000.00,
  "warrant_amount": 5000.00,
  "rent_start_date": "2026-05-01",
  "rent_end_date": "2027-04-30",
  "rent_period": 12,
  "contract_url": "https://example.com/contract.pdf",
  "customer_id_url": "https://example.com/id.jpg",
  "commission": 500.00,
  "rent_price": 2500.00
}
```

### 2.4 Example: update customer source

**PUT** `/rental-contracts/10`

```json
{
  "how_did_customer_find_us": "Aqar map"
}
```

```json
{
  "how_did_customer_find_us": "Dubizzle"
}
```

---

## 3. Database migrations (operational)

Apply these on your MySQL database when upgrading an existing deployment (dev/staging/prod). Adjust only if your schema was created differently.

### 3.1 `location` columns (apartments)

```sql
ALTER TABLE apartment_sales
  MODIFY COLUMN location VARCHAR(255) NOT NULL;

ALTER TABLE apartment_rents
  MODIFY COLUMN location VARCHAR(255) NOT NULL;
```

### 3.2 `how_did_customer_find_us` (rental contracts)

The column must allow the new enum values. One possible definition:

```sql
ALTER TABLE rental_contracts
  MODIFY COLUMN how_did_customer_find_us ENUM(
    'facebook',
    'instagram',
    'google',
    'Bayut',
    'Aqar map',
    'Dubizzle',
    'referral',
    'walk_in',
    'other'
  ) NOT NULL;
```

**Note:** If you add values only in code but not in MySQL, inserts can fail with enum/truncation errors.

---

## 4. Source files touched (reference)

| Area | Files (non-exhaustive) |
|------|-------------------------|
| Models | `models/apartment_rent.py`, `models/apartment_sale.py`, `models/rental_contract.py`, `models/enums.py` |
| Schemas | `schemas/apartment_rent.py`, `schemas/apartment_sale.py`, `schemas/enums.py` |
| Routers | `routers/apartments.py` (sale `PUT` import/handler name fix) |
| Setup | `setup.py` (sample `location` strings) |
| Docs (same session) | `FRONTEND_INTEGRATION_GUIDE.md`, `TESTING.md` (location text; customer source list may still be updated elsewhere to match section 2) |

---

## 5. Quick verification (curl)

**Login** (form body):

```bash
curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your@email.com&password=yourpassword"
```

**Apartment sale** with arbitrary `location`:

```bash
curl -s -X POST "http://localhost:8000/api/v1/apartments/sale" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","location":"Any Area Name","address":"A","area":10,"number":"1","price":1000,"bedrooms":1,"bathrooms":"private"}'
```

**Rental contract** with `how_did_customer_find_us: "Dubizzle"` (requires valid `apartment_part_id`):

```bash
curl -s -X POST "http://localhost:8000/api/v1/rental-contracts/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"apartment_part_id":1,"customer_name":"X","customer_phone":"+201111111111","customer_id_number":"1","how_did_customer_find_us":"Dubizzle","paid_deposit":1,"warrant_amount":1,"rent_start_date":"2026-01-01","rent_end_date":"2026-12-31","rent_period":12,"commission":1,"rent_price":1}'
```

---

## 6. Related documentation

- **`TESTING.md`** — end-to-end test data and enum sections  
- **`FRONTEND_INTEGRATION_GUIDE.md`** — field mapping and client pitfalls  
- **`API_DOCUMENTATION.md`** — full endpoint reference  

This file is a **delta** for the changes above; the three guides remain the main long-form references unless they are updated to match.
