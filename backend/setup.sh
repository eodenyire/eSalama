#!/bin/bash

# eSalama Backend Setup Script

echo "==================================="
echo "eSalama Backend Setup"
echo "==================================="

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "==================================="
echo "✓ Backend setup complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env: cp .env.example .env"
echo "2. Update .env with your database credentials and secrets"
echo "3. Set up PostgreSQL database: createdb esalama"
echo "4. Run the server: uvicorn src.main:app --reload"
echo ""
echo "The API will be available at http://localhost:8000"
echo "API docs at http://localhost:8000/docs"
