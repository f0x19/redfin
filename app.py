from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'realestate_db'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'port': os.getenv('DB_PORT', 3306)
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize the database with tables"""
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database")
        return
    
    cursor = connection.cursor()
    
    try:
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create properties table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
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
            )
        """)
        
        # Create favorites table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id INT AUTO_INCREMENT PRIMARY KEY,
                property_id INT NOT NULL,
                user_email VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE,
                UNIQUE KEY unique_favorite (property_id, user_email)
            )
        """)
        
        # Insert sample data if table is empty
        cursor.execute("SELECT COUNT(*) FROM properties")
        count = cursor.fetchone()[0]
        
        if count == 0:
            sample_properties = [
                ('Modern Downtown Condo', 'Beautiful modern condo in the heart of downtown with stunning city views. Features include hardwood floors, stainless steel appliances, and in-unit washer/dryer.', 
                 675000, '123 Main St', 'San Francisco', 'CA', '94102', 2, 2.0, 1200, 0, 2020, 'Condo', 'sale', 'active', 
                 'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800'),
                
                ('Spacious Family Home', 'Gorgeous 4-bedroom family home in excellent school district. Large backyard, updated kitchen, and finished basement perfect for entertaining.', 
                 825000, '456 Oak Avenue', 'Seattle', 'WA', '98101', 4, 3.0, 2800, 7500, 2015, 'Single Family', 'sale', 'active',
                 'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800'),
                
                ('Luxury Waterfront Estate', 'Stunning waterfront property with private dock and panoramic ocean views. Chef\'s kitchen, home theater, and infinity pool.', 
                 2500000, '789 Beach Road', 'Miami', 'FL', '33139', 5, 4.5, 4500, 12000, 2018, 'Single Family', 'sale', 'active',
                 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800'),
                
                ('Cozy Starter Home', 'Perfect starter home in quiet neighborhood. Recently renovated with new roof, windows, and HVAC system. Move-in ready!', 
                 350000, '321 Maple Street', 'Austin', 'TX', '78701', 3, 2.0, 1500, 5000, 2005, 'Single Family', 'sale', 'active',
                 'https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=800'),
                
                ('Urban Loft with Character', 'Industrial-style loft in converted warehouse. Exposed brick, high ceilings, and modern amenities. Walking distance to restaurants and shops.', 
                 550000, '654 Industrial Blvd', 'Denver', 'CO', '80202', 1, 1.0, 900, 0, 1995, 'Loft', 'sale', 'active',
                 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800'),
                
                ('Mountain View Ranch', 'Beautiful ranch-style home with breathtaking mountain views. Open floor plan, vaulted ceilings, and expansive deck for outdoor living.', 
                 695000, '987 Ridge Road', 'Boulder', 'CO', '80301', 3, 2.5, 2200, 10000, 2012, 'Single Family', 'sale', 'active',
                 'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800'),
                
                ('Historic Victorian Home', 'Meticulously restored Victorian with original details. Wrap-around porch, turret, and modern updates throughout while maintaining historic charm.', 
                 775000, '147 Heritage Lane', 'Portland', 'OR', '97201', 4, 3.0, 3000, 6000, 1890, 'Single Family', 'sale', 'active',
                 'https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800'),
                
                ('Contemporary Townhouse', 'Brand new townhouse in desirable neighborhood. Open concept living, rooftop terrace, and attached 2-car garage.', 
                 485000, '258 Park Place', 'Chicago', 'IL', '60614', 3, 2.5, 1800, 0, 2023, 'Townhouse', 'sale', 'active',
                 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800'),
            ]
            
            cursor.executemany("""
                INSERT INTO properties (title, description, price, address, city, state, zip_code, 
                                      bedrooms, bathrooms, square_feet, lot_size, year_built, 
                                      property_type, listing_type, status, image_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_properties)
        
        connection.commit()
        print("Database initialized successfully!")
        
    except Error as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
        connection.close()

# Routes
@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/property/<int:property_id>')
def property_detail(property_id):
    """Render property detail page"""
    return render_template('property_detail.html')

@app.route('/api/properties', methods=['GET'])
def get_properties():
    """Get all properties with optional filters"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get filter parameters
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        bedrooms = request.args.get('bedrooms', type=int)
        bathrooms = request.args.get('bathrooms', type=float)
        property_type = request.args.get('property_type')
        city = request.args.get('city')
        search = request.args.get('search')
        
        # Build query
        query = "SELECT * FROM properties WHERE status = 'active'"
        params = []
        
        if min_price:
            query += " AND price >= %s"
            params.append(min_price)
        
        if max_price:
            query += " AND price <= %s"
            params.append(max_price)
        
        if bedrooms:
            query += " AND bedrooms >= %s"
            params.append(bedrooms)
        
        if bathrooms:
            query += " AND bathrooms >= %s"
            params.append(bathrooms)
        
        if property_type:
            query += " AND property_type = %s"
            params.append(property_type)
        
        if city:
            query += " AND city LIKE %s"
            params.append(f"%{city}%")
        
        if search:
            query += " AND (title LIKE %s OR description LIKE %s OR address LIKE %s OR city LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param, search_param])
        
        query += " ORDER BY created_at DESC"
        
        cursor.execute(query, params)
        properties = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for prop in properties:
            prop['price'] = float(prop['price'])
            prop['bathrooms'] = float(prop['bathrooms'])
            if prop['created_at']:
                prop['created_at'] = prop['created_at'].isoformat()
            if prop['updated_at']:
                prop['updated_at'] = prop['updated_at'].isoformat()
        
        return jsonify(properties)
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """Get a single property by ID"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM properties WHERE id = %s", (property_id,))
        property_data = cursor.fetchone()
        
        if not property_data:
            return jsonify({'error': 'Property not found'}), 404
        
        # Convert Decimal to float for JSON serialization
        property_data['price'] = float(property_data['price'])
        property_data['bathrooms'] = float(property_data['bathrooms'])
        if property_data['created_at']:
            property_data['created_at'] = property_data['created_at'].isoformat()
        if property_data['updated_at']:
            property_data['updated_at'] = property_data['updated_at'].isoformat()
        
        return jsonify(property_data)
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/properties', methods=['POST'])
def create_property():
    """Create a new property listing"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    data = request.json
    
    try:
        cursor.execute("""
            INSERT INTO properties (title, description, price, address, city, state, zip_code,
                                  bedrooms, bathrooms, square_feet, lot_size, year_built,
                                  property_type, listing_type, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['title'], data.get('description'), data['price'], data['address'],
            data['city'], data['state'], data['zip_code'], data['bedrooms'],
            data['bathrooms'], data['square_feet'], data.get('lot_size'),
            data.get('year_built'), data['property_type'], data['listing_type'],
            data.get('image_url')
        ))
        
        connection.commit()
        property_id = cursor.lastrowid
        
        return jsonify({'id': property_id, 'message': 'Property created successfully'}), 201
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """Add a property to favorites"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor()
    data = request.json
    
    try:
        cursor.execute("""
            INSERT INTO favorites (property_id, user_email)
            VALUES (%s, %s)
        """, (data['property_id'], data['user_email']))
        
        connection.commit()
        
        return jsonify({'message': 'Property added to favorites'}), 201
        
    except Error as e:
        if 'Duplicate entry' in str(e):
            return jsonify({'error': 'Property already in favorites'}), 400
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/api/favorites/<user_email>', methods=['GET'])
def get_favorites(user_email):
    """Get favorite properties for a user"""
    connection = get_db_connection()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT p.* FROM properties p
            INNER JOIN favorites f ON p.id = f.property_id
            WHERE f.user_email = %s
            ORDER BY f.created_at DESC
        """, (user_email,))
        
        properties = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for prop in properties:
            prop['price'] = float(prop['price'])
            prop['bathrooms'] = float(prop['bathrooms'])
            if prop['created_at']:
                prop['created_at'] = prop['created_at'].isoformat()
            if prop['updated_at']:
                prop['updated_at'] = prop['updated_at'].isoformat()
        
        return jsonify(properties)
        
    except Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    # Initialize database on startup
    init_db()
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
