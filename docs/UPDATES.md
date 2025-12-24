# Exarth Company Site - Project Updates

## 18th Dec, 2025

- ✅ Updated README.md (confidential notice, installation guide, project structure)
- ✅ Updated .env files in docs/configs/ (.env, .env.example, .env.production)
- ✅ Updated all bash scripts in docs/bash/ for this project's apps

### Changes Made:

#### README.md
- Added confidential notice
- Complete installation guide (script & manual)
- Project structure documentation for Exarth Company Site
- Environment variables documentation (django-environ)
- Bash scripts usage guide
- Database migrations guide
- Admin access instructions
- Running the server guide
- Apps overview table

#### docs/configs/
- `.env.example` - Template for developers with all required variables
- `.env` - Development environment settings
- `.env.production` - Production environment template

Required environment variables:
- `DEBUG`, `SECRET_KEY`, `ENVIRONMENT`, `SITE_ID`
- `DOMAIN`, `PROTOCOL`, `ALLOWED_HOSTS`
- `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`
- `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`
- `DEFAULT_FROM_EMAIL`, `MAILCHIMP_API_KEY`, `MAILCHIMP_FROM_EMAIL`

#### docs/bash/
All scripts now work from ANY directory using `SCRIPT_DIR` and `PROJECT_ROOT`:
- `setup.sh` - Complete project setup (venv, deps, migrations, static)
- `migrations.sh` - Run migrations for all apps: company, projects, resources, services, website
- `migrations_clean.sh` - Clean all migration files with confirmation (handles src/services/* and src/website/ paths)
- `requirements.sh` - Install/update Python dependencies
- `static.sh` - Collect static files
- `superuser.sh` - Create admin superuser (uses get_user_model for flexibility)

### Apps Structure:
```
src/
├── services/
│   ├── company/       # Company info, team, about
│   ├── projects/      # Portfolio and projects
│   ├── resources/     # Resources management
│   └── services/      # Service offerings
└── website/           # Main website, homepage, contact
```

### Note:
Run `chmod +x docs/bash/*.sh` to make scripts executable before first use.
