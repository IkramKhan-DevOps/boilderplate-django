#!/bin/bash
# =============================================================================
# EXARTH COMPANY SITE - Initial Setup Script
# =============================================================================
# Description: Complete project setup including venv, dependencies, migrations
# Usage: ./docs/bash/setup.sh (from any directory)
# =============================================================================

set -e  # Exit on error

# Get the project root directory (2 levels up from docs/bash/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"
echo "📁 Working in: $PROJECT_ROOT"

echo ""
echo "=========================================="
echo "   EXARTH COMPANY SITE - INITIAL SETUP"
echo "=========================================="
echo ""

# Step 1: Create virtual environment
echo "🔧 Step 1: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ⏭️  Virtual environment already exists"
fi

# Step 2: Activate virtual environment
echo "🔧 Step 2: Activating virtual environment..."
source venv/bin/activate
echo "   ✅ Virtual environment activated"

# Step 3: Install requirements
echo "🔧 Step 3: Installing requirements..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo "   ✅ Requirements installed"

# Step 4: Copy .env file if not exists
echo "🔧 Step 4: Setting up environment file..."
if [ ! -f ".env" ]; then
    cp docs/configs/.env .env
    echo "   ✅ .env file created from template"
else
    echo "   ⏭️  .env file already exists"
fi

# Step 5: Make migrations
echo "🔧 Step 5: Making migrations..."
python manage.py makemigrations company
python manage.py makemigrations projects
python manage.py makemigrations resources
python manage.py makemigrations services
python manage.py makemigrations website
echo "   ✅ Migrations created"

# Step 6: Apply migrations
echo "🔧 Step 6: Applying migrations..."
python manage.py migrate
echo "   ✅ Migrations applied"

# Step 7: Collect static files
echo "🔧 Step 7: Collecting static files..."
python manage.py collectstatic --noinput
echo "   ✅ Static files collected"

# Step 8: Create superuser (optional)
echo ""
read -p "🔧 Step 8: Do you want to create a superuser? (y/N): " create_superuser

if [[ "$create_superuser" == "y" || "$create_superuser" == "Y" ]]; then
    echo ""
    echo "Default credentials: email=mark@exarth.com, username=mark, password=mark"
    read -p "   Use default credentials? (Y/n): " use_default

    if [[ "$use_default" == "n" || "$use_default" == "N" ]]; then
        python manage.py createsuperuser
    else
        python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='mark@exarth.com').exists():
    User.objects.create_superuser(
        email='mark@exarth.com',
        username='mark',
        password='mark'
    )
    print('   ✅ Superuser created successfully!')
else:
    print('   ⏭️  Superuser with this email already exists.')
EOF
    fi
else
    echo "   ⏭️  Skipping superuser creation"
fi

echo ""
echo "=========================================="
echo "   ✅ SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
