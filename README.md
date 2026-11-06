# AO Real Estate API

FastAPI + MySQL backend. Runs in containers only.

## Run

```bash
cp .env.example .env      # then set MYSQL_*, SECRET_KEY, BOOTSTRAP_ADMIN_*
docker compose up -d --build
curl localhost:${API_PORT:-8000}/health
```

Interactive docs: `http://localhost:<API_PORT>/docs`. API prefix: `/api/v1`.

- `SECRET_KEY` is required (compose refuses to start without it). Generate one with
  `python3 -c "import secrets; print(secrets.token_urlsafe(48))"`.
- The first super admin is created at startup from `BOOTSTRAP_ADMIN_EMAIL/PHONE/PASSWORD`
  when no super admin exists. Remove the password from `.env` afterwards.
- Data lives in the `mysql_data` and `uploads_data` volumes. `docker compose down` keeps them;
  `docker compose down -v` deletes them.
- The database port is not published to the host.

## Deploying on DigitalOcean App Platform

`.do/app.yaml` describes the whole site: this API, the frontend, and a managed MySQL cluster. Routing is done
by the platform: `/api` and `/uploads` go to the API, everything else to the frontend, so the browser only ever
talks to one domain (no CORS).

1. Create a **managed MySQL 8** cluster (Databases) in the same region.
2. Push the backend and frontend to GitHub (two repos, or adapt the spec).
3. Fill in the `TODO`s in `.do/app.yaml` (repo names, cluster name, bucket, admin email) and create the app
   (`doctl apps create --spec .do/app.yaml` or paste it into the console).
4. In the console set the secrets: `SECRET_KEY`, `BOOTSTRAP_ADMIN_PASSWORD`, `S3_ACCESS_KEY_ID`,
   `S3_SECRET_ACCESS_KEY`.
5. Add your domain, then log in with the bootstrap admin and change its password.

DigitalOcean's `DATABASE_URL` ends in `?ssl-mode=REQUIRED`; the API translates that into an encrypted
connection (set `DATABASE_SSL_CA` to a CA file path to also verify the server certificate).
App Platform disks are ephemeral, so uploaded files must go to a bucket (below).

Environment variables:

| Var | Notes |
|---|---|
| `DATABASE_URL` | `mysql://user:pass@host:port/db` (`mysql+pymysql://` is added automatically) |
| `SECRET_KEY` | long random string; with `ENVIRONMENT=production` the app refuses the insecure default |
| `ENVIRONMENT` | `production` |
| `CORS_ORIGINS` | only needed if a different origin calls the API directly |
| `BOOTSTRAP_ADMIN_*` | first super admin (created once, if no super admin exists) |
| `STORAGE_BACKEND` | `local` (Docker volume, development) or `s3` |
| `MAX_UPLOAD_MB` | default 10; allowed types: jpg, jpeg, png, gif, webp, pdf |

## Storing files in AWS S3

The API uploads files to the bucket and returns the full URL of each one (`photos_url` on apartments and
studios). The frontend uses those URLs directly as `<img src>`; it never talks to S3 itself, so the bucket
needs no CORS configuration.

Set in `.env` / the hosting dashboard:

```
STORAGE_BACKEND=s3
S3_BUCKET=your-bucket-name
S3_REGION=eu-central-1
S3_ACCESS_KEY_ID=...        # IAM user access key (see policy below)
S3_SECRET_ACCESS_KEY=...
# optional: S3_PUBLIC_BASE_URL=https://cdn.example.com   (CloudFront / custom domain; defaults to the bucket URL)
# optional: S3_KEY_PREFIX=ao                              (store everything under a folder)
```

Leave `S3_ENDPOINT_URL` empty for AWS. (It exists only for other S3-compatible providers such as
DigitalOcean Spaces, e.g. `https://fra1.digitaloceanspaces.com`.) On startup the API logs `File storage ready: S3Storage`, or the
reason it can't reach the bucket.

**1. IAM user** with only this policy (access keys are created for this user):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
      "Resource": "arn:aws:s3:::YOUR_BUCKET/*" },
    { "Effect": "Allow", "Action": ["s3:ListBucket"], "Resource": "arn:aws:s3:::YOUR_BUCKET" }
  ]
}
```

**2. Public read for listing photos only.** In the bucket, turn off *Block public access* (at least
"block public bucket policies"), then add this bucket policy. Contract and customer-ID files
(`rental_contract/`) are deliberately **not** listed, so they stay private:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow", "Principal": "*", "Action": "s3:GetObject",
    "Resource": ["arn:aws:s3:::YOUR_BUCKET/part/*", "arn:aws:s3:::YOUR_BUCKET/rent/*", "arn:aws:s3:::YOUR_BUCKET/sale/*"]
  }]
}
```

(With `S3_KEY_PREFIX=ao`, use `YOUR_BUCKET/ao/part/*` etc.)

Private files are opened through `GET /api/v1/uploads/signed-url?url=<stored url>`, which returns a link that
expires (15 min by default).

### What gets deleted from the bucket
- `DELETE /api/v1/uploads/photos?entity_type=&entity_id=&url=` removes one photo (or, for `rental_contract`, a
  `document_type=contract|customer_id` document).
- Editing a listing/studio with a shorter `photos_url` deletes the dropped files.
- Deleting an apartment, studio, sale listing or contract deletes all of its files. Deleting an apartment or
  studio that still has a rental contract is refused with 400 until the contract is deleted.
- Only the admin who created an item (or a super admin) can upload/delete its files.
