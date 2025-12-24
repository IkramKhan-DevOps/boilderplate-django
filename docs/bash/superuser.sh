#!/bin/bash
# =============================================================================
# EXARTH COMPANY SITE - Create Superuser Script
# =============================================================================
# Description: Create Django admin superuser
# Usage: ./docs/bash/superuser.sh (from any directory)
# Default credentials: email: mark@exarth.com, username: mark, password: mark
# =============================================================================

set -e  # Exit on error

# Get the project root directory (2 levels up from docs/bash/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"
echo "📁 Working in: $PROJECT_ROOT"

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Error: Virtual environment not found. Run setup.sh first."
    exit 1
fi

echo ""
echo "=========================================="
echo "   CREATE SUPERUSER"
echo "=========================================="
echo ""

# Check if user wants to use default or custom credentials
echo "Default credentials:"
echo "  Email: mark@exarth.com"
echo "  Username: mark"
echo "  Password: mark"
echo ""
read -p "Use default credentials? (Y/n): " use_default

if [[ "$use_default" == "n" || "$use_default" == "N" ]]; then
    echo ""
    echo "🔧 Creating superuser with custom credentials..."
    python manage.py createsuperuser
else
    echo ""
    echo "🔧 Creating superuser with default credentials..."

    # Create superuser non-interactively
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

echo ""
echo "=========================================="
echo "   ✅ SUPERUSER SETUP COMPLETE!"
echo "=========================================="
echo ""
echo "You can now login at: /admin/"
echo ""

