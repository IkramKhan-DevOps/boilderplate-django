#!/bin/bash
# =============================================================================
# EXARTH COMPANY SITE - Migrations Script
# =============================================================================
# Description: Run migrations for all apps in sequence
# Usage: ./docs/bash/migrations.sh (from any directory)
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
echo "   RUNNING MIGRATIONS"
echo "=========================================="
echo ""

# Make migrations for each app in sequence
echo "🔧 Making migrations for company..."
python manage.py makemigrations company

echo "🔧 Making migrations for projects..."
python manage.py makemigrations projects

echo "🔧 Making migrations for resources..."
python manage.py makemigrations resources

echo "🔧 Making migrations for services..."
python manage.py makemigrations services

echo "🔧 Making migrations for website..."
python manage.py makemigrations website

echo ""
echo "🔧 Applying all migrations..."
python manage.py migrate

echo ""
echo "=========================================="
echo "   ✅ MIGRATIONS COMPLETE!"
echo "=========================================="
echo ""
