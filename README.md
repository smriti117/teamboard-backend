# TeamBoard Backend

Django + DRF backend powering TeamBoard's Knowledge Base API: company
registration, JWT auth, keyword search over Q&A entries, and a
platform-admin usage dashboard.

## Stack

- Django + Django REST Framework
- PostgreSQL (via Docker)
- SimpleJWT for authentication

## 1. Set up the database (Docker)

Copy the example env file and fill in real values:

```bash
cp .env.example .env
```

Start Postgres:

```bash
docker compose up -d
```

This launches a `postgres:16` container using the credentials from `.env`
and persists data in a named volume (`teamboard_pgdata`).

## 2. Install dependencies

```bash
conda create --name teamboard

conda activate teamboard

pip install -r requirements.txt
```

## 3. Apply migrations

```bash
python manage.py migrate
```

## 4. Seed the knowledge base

```bash
python manage.py seed_kb
```

This loads 12 sample Q&A entries across all five categories, with
overlapping keywords (e.g. `select_related` / `prefetch_related`) so
search returns multiple results.

And CreateSuperUser:

```
 python3 manage.py createsuperuser
```

username : admin
email : admin@gmail.com
password : admin

## 5. Run the server

```bash
python manage.py runserver
```

The API is now available at `http://localhost:8000/api/`.

## Endpoints

| Method | Path                        | Auth      | Purpose                               |
| ------ | --------------------------- | --------- | ------------------------------------- |
| POST   | `/api/auth/register/`       | Public    | Register a company, get JWT + API key |
| POST   | `/api/auth/login/`          | Public    | Log in, get a fresh JWT               |
| POST   | `/api/kb/query/`            | JWT       | Search the knowledge base (logged)    |
| GET    | `/api/admin/usage-summary/` | JWT+Admin | Platform usage stats                  |

For protected endpoints, send the token as:
`Authorization: Bearer <access_token>`

## Promoting a company to ADMIN

The `role` field can't be set via the API by design. To view the usage
dashboard, flip a company's role directly in the database (e.g. via
PGAdmin or `psql`):

```sql
UPDATE api_company SET role = 'admin' WHERE company_name = 'CompanyOne Pvt Ltd';
```

Then log in again to use that account against
`/api/admin/usage-summary/`.

## Project layout

```
config/          Django project settings, root URLs
api/
  models.py      Company, KBEntry, QueryLog
  signals.py     post_save signal: auto-creates Company + api_key
  apps.py        connects the signal in AppConfig.ready()
  permissions.py IsAdminUser (checks Company.role == ADMIN)
  serializers.py KBEntry output shape
  views.py       the 4 endpoint views
  urls.py        api app routes
  management/commands/seed_kb.py
```
