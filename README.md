# Dogwood Seniors 50 Plus — Backend

Backend API for the Dogwood Seniors 50 Plus website. Built with Django + Django REST Framework, deployed to AWS.

---

## Prerequisites

You need these installed on your computer before anything else:

| Tool | What it is | Install |
|------|-----------|---------|
| **Git** | Version control | [git-scm.com](https://git-scm.com/) |
| **Docker Desktop** | Runs containers (app + database) | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) |
| **Python 3.12+** | For running linter/tests outside Docker | [python.org](https://www.python.org/downloads/) |

---

## Local Development Setup

### 1. Clone the repo

```bash
git clone git@github.com:YOUR-ORG/dogwood-backend.git
cd dogwood-backend
```

### 2. Start the app

```bash
docker compose up
```

This starts two things:
- **PostgreSQL database** on port 5432
- **Django dev server** on port 8000

Wait until you see `Starting development server at http://0.0.0.0:8000/`

### 3. Run initial database setup (first time only)

Open a **new terminal** tab:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

`migrate` creates all the database tables. `createsuperuser` asks you to pick an admin email and password.

### 4. Open the app

- **Admin panel**: http://localhost:8000/admin/ — log in with the superuser you just created
- **API root**: http://localhost:8000/api/v1/ — empty for now, endpoints come in Week 3

### 5. Stop the app

```bash
docker compose down
```

Add `-v` to also delete the database data: `docker compose down -v`

---

## Running Tests & Linting Locally

Install dev dependencies in a virtual environment:

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements/dev.txt
```

Then run:

```bash
# Lint (checks code style)
ruff check .
ruff format --check .

# Tests (needs the database running via docker compose up)
pytest --cov=apps --cov-fail-under=80
```

---

## Project Structure

```
dogwood-backend/
  config/                    # Django settings, URLs, WSGI
    settings/
      base.py                # Shared settings
      dev.py                 # Local development overrides
      prod.py                # Production overrides
    urls.py                  # URL routing
    wsgi.py                  # Entry point for Gunicorn
  apps/
    content/                 # Pages, Posts, Attachments
    activities/              # Categories, Activity Groups
    community/               # Community Support Resources
    info/                    # Board Members, Contact Form, Subscriptions
  tests/                     # All test files
  requirements/
    base.txt                 # Shared dependencies
    dev.txt                  # Dev-only (pytest, ruff)
    prod.txt                 # Prod-only
  Dockerfile                 # Container build instructions
  docker-compose.yml         # Local dev environment
  pyproject.toml             # Pytest + Ruff config
  .github/workflows/
    ci.yml                   # Lint + test on every push
    deploy.yml               # Deploy to EC2 on push to main
```

---

## Branch Rules

| Branch | Purpose | Who merges here |
|--------|---------|-----------------|
| `main` | Production-ready code | PR only, 1 review + CI passing |
| `develop` | Integration branch | Feature PRs merge here |
| `feature/*` | Individual work | Created from `develop` |

**Workflow**: Create `feature/your-thing` from `develop` → do your work → open PR to `develop` → after review, merge → when `develop` is stable, PR to `main` → auto-deploys.

---

## Environment Variables

These are set automatically in Docker. On production (EC2), they live in AWS SSM Parameter Store.

| Variable | What it is | Example |
|----------|-----------|---------|
| `DJANGO_SETTINGS_MODULE` | Which settings file to use | `config.settings.prod` |
| `DJANGO_SECRET_KEY` | Random secret for security | (long random string) |
| `DB_NAME` | Database name | `dogwood` |
| `DB_USER` | Database username | `dogwood` |
| `DB_PASSWORD` | Database password | (from SSM) |
| `DB_HOST` | Database hostname | `dogwood-db.xxxxx.ca-central-1.rds.amazonaws.com` |
| `DB_PORT` | Database port | `5432` |
| `ALLOWED_HOSTS` | Comma-separated domains | `dogwoodseniors50plus.com,www.dogwoodseniors50plus.com` |
