# Exarth Company Site - Corporate Website

> **CONFIDENTIAL** - This repository contains proprietary code for Exarth Corporation. Unauthorized distribution or use is prohibited.

## About Exarth

EXARTH is a Software Development Corporation originated in Pakistan, which aims to bring the people with most incredible skill sets and ideas together to fulfill the needs of the 21st century. Here at Exarth, efforts are being made to make our tomorrow brighter than today - that's why we want each step of Exarth to be in the right direction.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip (Python package manager)
- Git

### Installation

#### Option 1: Using Setup Script (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Exarth-Company-Site

# Run the setup script
chmod +x docs/bash/setup.sh
./docs/bash/setup.sh
```

#### Option 2: Manual Installation

```bash
# Clone the repository
git clone <repository-url>
cd Exarth-Company-Site

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp docs/configs/.env .env

# Run migrations
python manage.py makemigrations company projects resources services website
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

---

## 📁 Project Structure

```
Exarth-Company-Site/
├── root/                   # Django project settings
│   ├── settings.py         # Main settings file
│   ├── urls.py             # Root URL configuration
│   ├── context_processor.py # Custom context processors
│   └── wsgi.py             # WSGI configuration
├── src/                    # Application modules
│   ├── services/           # Services submodules
│   │   ├── company/        # Company information
│   │   ├── projects/       # Projects portfolio
│   │   ├── resources/      # Resources management
│   │   └── services/       # Services offerings
│   └── website/            # Public website
├── templates/              # HTML templates
├── static/                 # Static assets (CSS, JS, images)
├── media/                  # User-uploaded files
├── docs/                   # Documentation & scripts
│   ├── bash/               # Bash utility scripts
│   └── configs/            # Configuration templates
└── manage.py               # Django management script
```

---

## 🔧 Configuration

### Environment Variables

The project uses `django-environ` for environment variable management. Create a `.env` file in the project root:

```bash
cp docs/configs/.env.example .env
```

Key environment variables:

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

---

## 📜 Bash Scripts

All scripts are located in `docs/bash/` and can be run from any directory:

```bash
# Make scripts executable (first time only)
chmod +x docs/bash/*.sh
```

| Script | Description |
|--------|-------------|
| `setup.sh` | Complete project setup (venv, deps, migrations, static) |
| `migrations.sh` | Run migrations for all apps |
| `migrations_clean.sh` | Clean all migration files (with confirmation) |
| `requirements.sh` | Install/update Python dependencies |
| `static.sh` | Collect static files |
| `superuser.sh` | Create admin superuser |

---

## 🗄️ Database Migrations

### Run migrations for all apps:

```bash
./docs/bash/migrations.sh
```

### Or manually:

```bash
python manage.py makemigrations company projects resources services website
python manage.py migrate
```

### Clean migrations (fresh start):

```bash
./docs/bash/migrations_clean.sh
```

---

## 👤 Admin Access

### Create superuser:

```bash
./docs/bash/superuser.sh
```

Default credentials (for development):
- **Email:** mark@exarth.com
- **Username:** mark
- **Password:** mark

Access admin panel at: `http://localhost:8000/admin/`

---

## 🖥️ Running the Server

### Development:

```bash
python manage.py runserver
```

### With specific port:

```bash
python manage.py runserver 0.0.0.0:8080
```

---

## 📦 Apps Overview

| App | Path | Description |
|-----|------|-------------|
| `company` | `src/services/company/` | Company info, team, about pages |
| `projects` | `src/services/projects/` | Portfolio and project showcase |
| `resources` | `src/services/resources/` | Resources and downloads |
| `services` | `src/services/services/` | Service offerings |
| `website` | `src/website/` | Main website, homepage, contact |

---

## 📄 License

This project is proprietary software owned by Exarth Corporation. All rights reserved.
