#!/bin/bash

# eSalama Admin Portal Setup Script

echo "==================================="
echo "eSalama Admin Portal Setup"
echo "==================================="

# Check Node version
echo ""
echo "Checking Node.js version..."
node --version

# Check npm version
echo ""
echo "Checking npm version..."
npm --version

# Install dependencies
echo ""
echo "Installing dependencies..."
npm install

echo ""
echo "==================================="
echo "✓ Frontend setup complete!"
echo "==================================="
echo ""
echo "Next steps:"
echo "1. Ensure backend is running at http://localhost:8000"
echo "2. Run the development server: npm run dev"
echo ""
echo "The admin portal will be available at http://localhost:3000"
