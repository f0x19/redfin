"""
Simple test script to verify the application setup
Run this after installing dependencies to check if everything works
"""

import sys
import subprocess

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing Python package imports...")
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError:
        print("✗ Flask import failed")
        return False
    
    try:
        import flask_cors
        print("✓ Flask-CORS imported successfully")
    except ImportError:
        print("✗ Flask-CORS import failed")
        return False
    
    try:
        import mysql.connector
        print("✓ MySQL Connector imported successfully")
    except ImportError:
        print("✗ MySQL Connector import failed")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting file structure...")
    
    import os
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        'templates/index.html',
        'templates/property_detail.html',
        'static/css/style.css',
        'static/js/main.js',
        'static/js/property_detail.js'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False
    
    return all_exist

def test_app_creation():
    """Test if Flask app can be created"""
    print("\nTesting Flask app creation...")
    
    try:
        from app import app
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("RealEstate Application Test Suite")
    print("=" * 50)
    print()
    
    results = []
    
    # Test imports
    results.append(("Package Imports", test_imports()))
    
    # Test file structure
    results.append(("File Structure", test_file_structure()))
    
    # Test app creation
    results.append(("Flask App", test_app_creation()))
    
    # Summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 All tests passed! Your application is ready to run.")
        print("\nTo start the application:")
        print("  1. Configure .env with your database credentials")
        print("  2. Run: python3 app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
