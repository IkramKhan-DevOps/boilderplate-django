#!/bin/bash
# =============================================================================
# EXARTH COMPANY SITE - Clean Migrations Script
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

# Clean migrations for each app
# Note: services apps are in src/services/, website is in src/website/
SERVICES_APPS=("company" "projects" "resources" "services")

for app in "${SERVICES_APPS[@]}"; do
    MIGRATION_DIR="src/services/$app/migrations"
    if [ -d "$MIGRATION_DIR" ]; then
        echo "🧹 Cleaning migrations for $app..."
        find "$MIGRATION_DIR" -type f -name "*.py" ! -name "__init__.py" -delete
        find "$MIGRATION_DIR" -type f -name "*.pyc" -delete
        # Clean __pycache__ inside migrations
        if [ -d "$MIGRATION_DIR/__pycache__" ]; then
            rm -rf "$MIGRATION_DIR/__pycache__"
        fi
        echo "   ✅ Cleaned $app migrations"
    else
        echo "   ⏭️  No migrations folder for $app"
    fi
done

# Clean website app (different path)
MIGRATION_DIR="src/website/migrations"
if [ -d "$MIGRATION_DIR" ]; then
    echo "🧹 Cleaning migrations for website..."
    find "$MIGRATION_DIR" -type f -name "*.py" ! -name "__init__.py" -delete
    find "$MIGRATION_DIR" -type f -name "*.pyc" -delete
    if [ -d "$MIGRATION_DIR/__pycache__" ]; then
        rm -rf "$MIGRATION_DIR/__pycache__"
    fi
    echo "   ✅ Cleaned website migrations"
else
    echo "   ⏭️  No migrations folder for website"
fi

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
