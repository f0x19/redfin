#!/usr/bin/env python3
"""
Example script to add custom properties to the database
This demonstrates how to use the API to add new property listings
"""

import requests
import json

# API endpoint
API_URL = "http://localhost:5000/api/properties"

# Example property data
example_properties = [
    {
        "title": "Stunning Modern Villa",
        "description": "Absolutely gorgeous modern villa with panoramic views, infinity pool, and state-of-the-art smart home features. Chef's kitchen with top-of-the-line appliances, spa-like master bathroom, and home theater.",
        "price": 1850000,
        "address": "1234 Hillside Drive",
        "city": "Los Angeles",
        "state": "CA",
        "zip_code": "90210",
        "bedrooms": 5,
        "bathrooms": 4.5,
        "square_feet": 4200,
        "lot_size": 15000,
        "year_built": 2021,
        "property_type": "Single Family",
        "listing_type": "sale",
        "image_url": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800"
    },
    {
        "title": "Downtown Penthouse Suite",
        "description": "Luxurious penthouse in premier downtown location. Floor-to-ceiling windows, private rooftop terrace, concierge service, and breathtaking city views. Walking distance to finest restaurants and entertainment.",
        "price": 2200000,
        "address": "789 Skyline Avenue",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001",
        "bedrooms": 3,
        "bathrooms": 3.0,
        "square_feet": 2800,
        "lot_size": 0,
        "year_built": 2019,
        "property_type": "Condo",
        "listing_type": "sale",
        "image_url": "https://images.unsplash.com/photo-1567496898669-ee935f5f647a?w=800"
    },
    {
        "title": "Charming Suburban Home",
        "description": "Move-in ready home in excellent family neighborhood. Recently updated kitchen and bathrooms, hardwood floors throughout, finished basement, and large fenced backyard perfect for kids and pets.",
        "price": 425000,
        "address": "456 Elm Street",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02101",
        "bedrooms": 4,
        "bathrooms": 2.5,
        "square_feet": 2200,
        "lot_size": 8000,
        "year_built": 2010,
        "property_type": "Single Family",
        "listing_type": "sale",
        "image_url": "https://images.unsplash.com/photo-1585914641050-fa9883c4e21c?w=800"
    }
]

def add_property(property_data):
    """
    Add a single property to the database via API
    """
    try:
        response = requests.post(
            API_URL,
            json=property_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✓ Added: {property_data['title']} (ID: {result['id']})")
            return True
        else:
            print(f"✗ Failed to add: {property_data['title']}")
            print(f"  Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the API.")
        print("  Make sure the Flask application is running (python3 app.py)")
        return False
    except Exception as e:
        print(f"✗ Error adding property: {e}")
        return False

def main():
    """
    Main function to add all example properties
    """
    print("=" * 60)
    print("Adding Custom Properties to RealEstate Database")
    print("=" * 60)
    print()
    
    # Check if API is accessible
    try:
        response = requests.get(API_URL)
        print(f"✓ API is accessible at {API_URL}")
        print(f"  Current properties in database: {len(response.json())}")
        print()
    except:
        print(f"✗ Cannot connect to API at {API_URL}")
        print("  Please make sure the Flask app is running:")
        print("  python3 app.py")
        return
    
    # Add each property
    print("Adding new properties...")
    print()
    
    success_count = 0
    for property_data in example_properties:
        if add_property(property_data):
            success_count += 1
    
    print()
    print("=" * 60)
    print(f"Added {success_count} out of {len(example_properties)} properties")
    print("=" * 60)
    print()
    
    if success_count > 0:
        print("Visit http://localhost:5000 to see the new properties!")

if __name__ == "__main__":
    main()


# Alternative: Direct database insertion (if API is not running)
"""
import mysql.connector
from mysql.connector import Error
import os

def add_property_direct(property_data):
    '''Add property directly to database'''
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'realestate_db'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            port=os.getenv('DB_PORT', 3306)
        )
        
        cursor = connection.cursor()
        
        cursor.execute('''
            INSERT INTO properties 
            (title, description, price, address, city, state, zip_code,
             bedrooms, bathrooms, square_feet, lot_size, year_built,
             property_type, listing_type, image_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            property_data['title'],
            property_data['description'],
            property_data['price'],
            property_data['address'],
            property_data['city'],
            property_data['state'],
            property_data['zip_code'],
            property_data['bedrooms'],
            property_data['bathrooms'],
            property_data['square_feet'],
            property_data['lot_size'],
            property_data['year_built'],
            property_data['property_type'],
            property_data['listing_type'],
            property_data['image_url']
        ))
        
        connection.commit()
        print(f"✓ Added: {property_data['title']}")
        
        cursor.close()
        connection.close()
        return True
        
    except Error as e:
        print(f"✗ Error: {e}")
        return False
"""
