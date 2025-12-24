#!/bin/bash
# =============================================================================
# DJANGO BOILERPLATE - Static Files Collection Script
# =============================================================================
# Description: Collect all static files for production
# Usage: ./docs/bash/static.sh (from any directory)
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
echo "   COLLECTING STATIC FILES"
echo "=========================================="
echo ""

echo "🔧 Running collectstatic..."
python manage.py collectstatic --noinput

echo ""
echo "=========================================="
echo "   ✅ STATIC FILES COLLECTED!"
echo "=========================================="
echo ""
echo "📁 Static files are collected in: $PROJECT_ROOT/assets/"
echo ""
