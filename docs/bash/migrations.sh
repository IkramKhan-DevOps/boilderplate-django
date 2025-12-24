#!/bin/bash
# =============================================================================
# DJANGO BOILERPLATE - Migrations Script
# =============================================================================
# Description: Run migrations for all apps
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

# Make migrations for all apps
echo "🔧 Making migrations..."
python manage.py makemigrations

echo ""
echo "🔧 Applying all migrations..."
python manage.py migrate

echo ""
echo "=========================================="
echo "   ✅ MIGRATIONS COMPLETE!"
echo "=========================================="
echo ""
