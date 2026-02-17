#!/bin/bash

# PostgreSQL Database Setup Script for Medical Chatbot
# This script sets up the PostgreSQL database and creates necessary tables

set -e

echo "================================================"
echo "Medical Chatbot - PostgreSQL Setup"
echo "================================================"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo -e "${RED}❌ PostgreSQL is not installed${NC}"
    echo "Install it with:"
    echo "  Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "  macOS: brew install postgresql"
    exit 1
fi

echo -e "${GREEN}✓ PostgreSQL is installed${NC}"

# Database credentials
DB_NAME="medical_db"
DB_USER="postgres"
DB_PASSWORD="tuhin1522"

echo ""
echo "Database Configuration:"
echo "  Database: $DB_NAME"
echo "  User: $DB_USER"
echo "  Password: $DB_PASSWORD"
echo ""

# Check if PostgreSQL service is running
if ! pg_isready -q; then
    echo -e "${YELLOW}⚠ PostgreSQL is not running${NC}"
    echo "Start it with:"
    echo "  Ubuntu/Debian: sudo systemctl start postgresql"
    echo "  macOS: brew services start postgresql"
    exit 1
fi

echo -e "${GREEN}✓ PostgreSQL is running${NC}"

# Create database (ignore error if already exists)
echo ""
echo "Creating database..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" 2>/dev/null || echo -e "${YELLOW}⚠ Database already exists${NC}"

# Grant privileges
echo "Granting privileges..."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" || true

echo -e "${GREEN}✓ Database setup complete${NC}"

# Create .env file
ENV_FILE="$(pwd)/.env"

if [ -f "$ENV_FILE" ]; then
    echo ""
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
    echo "Backing up to .env.backup"
    cp "$ENV_FILE" "$ENV_FILE.backup"
fi

# Generate secret key
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Create .env file
cat > "$ENV_FILE" << EOF
# Database Configuration
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME

# Security Configuration
SECRET_KEY=$SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Email Configuration (Optional - for production)
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
# SMTP_FROM=noreply@medicalchatbot.com
EOF

echo ""
echo -e "${GREEN}✓ .env file created${NC}"

# Test database connection
echo ""
echo "Testing database connection..."
if psql -U $DB_USER -d $DB_NAME -c "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Database connection successful${NC}"
else
    echo -e "${YELLOW}⚠ Could not connect to database${NC}"
    echo "You may need to update the password in .env file"
fi

echo ""
echo "================================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Review .env file and update if needed"
echo "  2. Start the server: python3 main.py"
echo "  3. Tables will be created automatically on first run"
echo "  4. Visit http://localhost:8000/docs to test API"
echo ""
echo "To test authentication:"
echo "  curl -X POST http://localhost:8000/auth/register \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"email\":\"test@example.com\",\"full_name\":\"Test User\",\"password\":\"test123456\"}'"
echo ""
