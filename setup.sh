#!/bin/bash

# RealEstate Website Setup Script

echo "=================================="
echo "RealEstate Website Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL client not found. Please ensure MySQL server is installed and running."
    echo "   You can install it with: sudo apt-get install mysql-server (Ubuntu/Debian)"
    echo "   or: brew install mysql (macOS)"
fi

echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Make sure MySQL server is running"
echo "2. Create a database: CREATE DATABASE realestate_db;"
echo "3. Copy .env.example to .env and update with your MySQL credentials"
echo "4. Run the application: python3 app.py"
echo ""
echo "The application will be available at: http://localhost:5000"
echo ""
