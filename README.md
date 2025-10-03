# RealEstate - Redfin-like Property Listing Website

A modern real estate listing website built with Flask, MySQL, HTML, CSS, and JavaScript. Features a clean, responsive design inspired by Redfin.

## Features

- 🏠 Browse property listings with beautiful card-based layout
- 🔍 Advanced search and filtering (price, bedrooms, bathrooms, property type, location)
- 📍 Interactive property detail pages
- ❤️ Favorite properties functionality
- 💰 Built-in mortgage calculator
- 📱 Fully responsive design
- 🎨 Modern UI with smooth animations

## Tech Stack

### Backend
- **Flask** - Python web framework
- **MySQL** - Database for storing property data
- **Flask-CORS** - Handle cross-origin requests

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with flexbox and grid
- **JavaScript** - Interactive features and API calls
- **Font Awesome** - Icon library

## Prerequisites

- Python 3.7+
- MySQL 5.7+ or MariaDB
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL Database

Start your MySQL server and create a database:

```sql
CREATE DATABASE realestate_db;
```

### 4. Configure Database Connection

Copy the example environment file and update with your database credentials:

```bash
cp .env.example .env
```

Edit `.env` file:

```
DB_HOST=localhost
DB_NAME=realestate_db
DB_USER=root
DB_PASSWORD=your_password
DB_PORT=3306
```

### 5. Initialize Database

The application will automatically create tables and insert sample data on first run. Alternatively, you can run:

```bash
python app.py
```

This will:
- Create the `properties` and `favorites` tables
- Insert 8 sample property listings
- Start the Flask development server

## Running the Application

```bash
python app.py
```

The application will be available at:
- **Frontend**: http://localhost:5000
- **API**: http://localhost:5000/api

## API Endpoints

### Properties

- `GET /api/properties` - Get all properties (with optional filters)
  - Query parameters: `min_price`, `max_price`, `bedrooms`, `bathrooms`, `property_type`, `city`, `search`
- `GET /api/properties/<id>` - Get single property by ID
- `POST /api/properties` - Create new property listing

### Favorites

- `POST /api/favorites` - Add property to favorites
- `GET /api/favorites/<user_email>` - Get user's favorite properties

## Project Structure

```
.
├── app.py                      # Flask application and API routes
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── templates/
│   ├── index.html             # Main property listing page
│   └── property_detail.html   # Property detail page
├── static/
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   ├── main.js            # Homepage JavaScript
│   │   └── property_detail.js # Property detail JavaScript
│   └── images/                # Static images (if any)
└── README.md                  # This file
```

## Database Schema

### Properties Table

```sql
CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(12, 2) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(50) NOT NULL,
    zip_code VARCHAR(20) NOT NULL,
    bedrooms INT NOT NULL,
    bathrooms DECIMAL(3, 1) NOT NULL,
    square_feet INT NOT NULL,
    lot_size INT,
    year_built INT,
    property_type VARCHAR(50) NOT NULL,
    listing_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Favorites Table

```sql
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (property_id, user_email)
);
```

## Features in Detail

### Search and Filtering
- Text search across title, description, address, and city
- Filter by price range
- Filter by minimum bedrooms and bathrooms
- Filter by property type (Single Family, Condo, Townhouse, Loft)
- Filter by city

### Property Listings
- Grid layout with property cards
- Property images from Unsplash
- Price, bedrooms, bathrooms, and square footage displayed
- Favorite button on each card
- Click to view detailed information

### Property Detail Page
- Large property image
- Comprehensive property information
- Interactive mortgage calculator
- Contact form to reach agents
- Schedule tour functionality

### Mortgage Calculator
- Calculate monthly payments
- Adjustable down payment percentage
- Configurable interest rate
- 15 or 30-year loan terms

## Customization

### Adding Your Own Properties

You can add properties via the API:

```bash
curl -X POST http://localhost:5000/api/properties \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Beautiful Home",
    "description": "A lovely property",
    "price": 500000,
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "bedrooms": 3,
    "bathrooms": 2.0,
    "square_feet": 2000,
    "lot_size": 5000,
    "year_built": 2020,
    "property_type": "Single Family",
    "listing_type": "sale",
    "image_url": "https://example.com/image.jpg"
  }'
```

### Changing Colors

Edit `static/css/style.css` and modify the CSS variables:

```css
:root {
    --primary-color: #c82021;  /* Main brand color */
    --secondary-color: #2d3748;
    --text-dark: #1a202c;
    --text-light: #718096;
}
```

## Production Deployment

For production deployment:

1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up a reverse proxy (Nginx, Apache)
3. Use environment variables for sensitive data
4. Enable SSL/TLS certificates
5. Configure proper MySQL user permissions
6. Set `debug=False` in app.py

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Troubleshooting

### Database Connection Issues

- Verify MySQL is running: `sudo service mysql status`
- Check credentials in `.env` file
- Ensure database exists: `SHOW DATABASES;`

### Port Already in Use

Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## License

MIT License - Feel free to use this project for personal or commercial purposes.

## Support

For issues or questions, please open an issue on the GitHub repository.

---

Built with ❤️ using Flask and MySQL
