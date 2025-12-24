#!/bin/bash
# =============================================================================
# DJANGO BOILERPLATE - Clean Migrations Script
# =============================================================================
# Description: Remove all migration files (except __init__.py) for fresh start
# Usage: ./docs/bash/migrations_clean.sh (from any directory)
# WARNING: This will delete all migration files! Use with caution.
# =============================================================================

set -e  # Exit on error

# Get the project root directory (2 levels up from docs/bash/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"
echo "📁 Working in: $PROJECT_ROOT"

echo ""
echo "=========================================="
echo "   CLEANING MIGRATIONS"
echo "=========================================="
echo ""
echo "⚠️  WARNING: This will delete all migration files!"
echo ""
read -p "Are you sure you want to continue? (y/N): " confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "❌ Operation cancelled."
    exit 0
fi

echo ""

# Find and clean all migrations in src directory
echo "🧹 Cleaning all migrations in src/..."
find "$PROJECT_ROOT/src" -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null || true
find "$PROJECT_ROOT/src" -path "*/migrations/*.pyc" -delete 2>/dev/null || true
find "$PROJECT_ROOT/src" -path "*/migrations/__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ Cleaned all migrations"

# Optionally remove database
echo ""
read -p "Do you also want to delete db.sqlite3? (y/N): " confirm_db

if [[ "$confirm_db" == "y" || "$confirm_db" == "Y" ]]; then
    if [ -f "db.sqlite3" ]; then
        rm db.sqlite3
        echo "   ✅ Database deleted"
    else
        echo "   ⏭️  No database file found"
    fi
fi

echo ""
echo "=========================================="
echo "   ✅ MIGRATIONS CLEANED!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Run migrations: ./docs/bash/migrations.sh"
echo ""
