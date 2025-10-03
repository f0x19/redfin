# Quick Start Guide

Get your RealEstate website up and running in 5 minutes!

## Prerequisites

- Python 3.7+
- MySQL 5.7+ or MariaDB
- pip

## Quick Setup

### Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# Copy environment file
cp .env.example .env

# Edit .env with your database credentials
nano .env  # or use your preferred editor

# Start the application
python3 app.py
```

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Configure database
cp .env.example .env
# Edit .env with your MySQL credentials

# 3. Create database (in MySQL)
mysql -u root -p
CREATE DATABASE realestate_db;
EXIT;

# 4. Run application
python3 app.py
```

## Access the Application

Once running, open your browser and navigate to:

**http://localhost:5000**

## Default Configuration

The application includes:
- ✅ 8 sample property listings
- ✅ Automatic database table creation
- ✅ Sample data insertion on first run

## Testing Features

### 1. Browse Properties
- Visit the homepage to see all listings
- Click on any property card to view details

### 2. Search and Filter
- Use the search bar to find properties by location
- Click "More Filters" to refine by price, bedrooms, bathrooms, etc.

### 3. Property Details
- Click any property to see:
  - Full description
  - Property specifications
  - Mortgage calculator
  - Contact form

### 4. Favorites
- Click the heart icon on any property to add to favorites
- View favorites count in the navigation bar

### 5. Mortgage Calculator
- On any property detail page
- Adjust down payment, interest rate, and loan term
- Click "Calculate" to see monthly payment estimate

## Troubleshooting

### Port 5000 Already in Use

Edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Connection Error

1. Check MySQL is running:
   ```bash
   sudo service mysql status
   ```

2. Verify credentials in `.env` file

3. Ensure database exists:
   ```bash
   mysql -u root -p -e "SHOW DATABASES;"
   ```

### Module Not Found Error

Reinstall dependencies:
```bash
pip3 install -r requirements.txt --upgrade
```

## Next Steps

- **Add Your Properties**: Use the API endpoints to add real property data
- **Customize Design**: Edit `static/css/style.css` to match your brand
- **Add Authentication**: Implement user login/signup for personalized features
- **Deploy**: Follow the production deployment guide in README.md

## Need Help?

Check the full documentation in `README.md` for:
- Detailed API documentation
- Database schema
- Customization options
- Production deployment guide

---

Happy listing! 🏠
