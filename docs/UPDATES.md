# Django Boilerplate - Documentation

## Overview

This is a production-ready Django boilerplate with authentication, REST API, and modern tooling.

## Features

- **Authentication**: django-allauth with social login (Google), MFA support
- **REST API**: Django REST Framework with dj-rest-auth
- **Forms**: Crispy Forms with Bootstrap 5
- **Email**: Mailchimp Transactional (Mandrill) integration
- **Phone**: Phone number field support
- **Filtering**: Django Filter for querysets
- **API Docs**: Swagger/OpenAPI via drf-yasg

## Project Structure

```
src/
├── core/               # Core utilities (models, helpers, signals, validators)
├── services/           # Backend services
│   ├── accounts/       # User accounts & authentication
│   └── dashboard/      # Dashboard functionality
└── web/                # Frontend web apps
    └── website/        # Public website
```

## Bash Scripts

All scripts are located in `docs/bash/` and can be run from any directory:

| Script | Description |
|--------|-------------|
| `setup.sh` | Complete project setup (venv, deps, migrations, static) |
| `migrations.sh` | Run migrations for all apps |
| `migrations_clean.sh` | Clean all migration files (with confirmation) |
| `requirements.sh` | Install/update Python dependencies |
| `static.sh` | Collect static files |
| `superuser.sh` | Create admin superuser |

### Usage

```bash
# Make scripts executable (first time only)
chmod +x docs/bash/*.sh

# Run any script
./docs/bash/setup.sh
./docs/bash/migrations.sh
./docs/bash/superuser.sh
```

## Environment Configuration

### Configuration Files

- `docs/configs/.env` - Development environment
- `docs/configs/.env.example` - Template for developers
- `docs/configs/.env.production` - Production environment template

### Required Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | Required |
| `ENVIRONMENT` | Environment type (`local`/`server`) | `local` |
| `DOMAIN` | Site domain | `localhost:8000` |
| `PROTOCOL` | HTTP or HTTPS | `http` |
| `ALLOWED_HOSTS` | Comma-separated list of hosts | `localhost,127.0.0.1` |
| `SITE_ID` | Django site ID | `1` |
| `DB_*` | Database configuration | SQLite (local) |

## Getting Started

1. Clone the repository
2. Run the setup script: `./docs/bash/setup.sh`
3. Start the server: `python manage.py runserver`
4. Access admin at: `http://localhost:8000/admin/`

### Default Superuser Credentials

- **Email:** admin@example.com
- **Username:** admin
- **Password:** admin

---

## Notes

Run `chmod +x docs/bash/*.sh` to make scripts executable before first use.
