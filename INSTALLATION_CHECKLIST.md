# Installation & Verification Checklist

Use this checklist to ensure your RealEstate website is properly set up and working.

## ✅ Pre-Installation Checklist

- [ ] Python 3.7+ installed
  ```bash
  python3 --version
  ```

- [ ] pip installed
  ```bash
  pip3 --version
  ```

- [ ] MySQL Server installed and running
  ```bash
  mysql --version
  # Test connection
  mysql -u root -p -e "SELECT VERSION();"
  ```

- [ ] Git installed (optional, for version control)
  ```bash
  git --version
  ```

## 📦 Installation Steps

### Step 1: Project Files
- [ ] All project files present (run this check)
  ```bash
  python3 test_app.py
  ```

### Step 2: Python Dependencies
- [ ] Install requirements
  ```bash
  pip3 install -r requirements.txt
  ```

- [ ] Verify installations
  ```bash
  python3 -c "import flask; print('Flask:', flask.__version__)"
  python3 -c "import mysql.connector; print('MySQL Connector: OK')"
  python3 -c "import flask_cors; print('Flask-CORS: OK')"
  ```

### Step 3: Database Setup
- [ ] Create database
  ```bash
  mysql -u root -p
  ```
  ```sql
  CREATE DATABASE realestate_db;
  SHOW DATABASES;
  EXIT;
  ```

- [ ] Verify database created
  ```bash
  mysql -u root -p -e "SHOW DATABASES LIKE 'realestate_db';"
  ```

### Step 4: Configuration
- [ ] Copy environment file
  ```bash
  cp .env.example .env
  ```

- [ ] Edit .env with your credentials
  ```bash
  nano .env  # or vim, code, etc.
  ```

- [ ] Verify .env contents
  ```bash
  cat .env
  ```

### Step 5: First Run
- [ ] Start the application
  ```bash
  python3 app.py
  ```

- [ ] Check console output for:
  - [ ] "Database initialized successfully!"
  - [ ] "Running on http://0.0.0.0:5000"

## 🧪 Verification Tests

### Test 1: Homepage Access
- [ ] Open browser to `http://localhost:5000`
- [ ] Homepage loads without errors
- [ ] See hero section with search bar
- [ ] See property cards in grid layout

### Test 2: Property Listings
- [ ] Properties displayed (should see 8 sample properties)
- [ ] Images load correctly
- [ ] Prices formatted with commas
- [ ] Property details visible (beds, baths, sqft)

### Test 3: Search Functionality
- [ ] Type "San Francisco" in search box
- [ ] Press Enter or click Search
- [ ] Results filter to San Francisco properties
- [ ] Results count updates

### Test 4: Filters
- [ ] Click "More Filters"
- [ ] Filter panel expands
- [ ] Set price range (e.g., $400,000 - $1,000,000)
- [ ] Click "Apply Filters"
- [ ] Results update accordingly
- [ ] Click "Clear All" - all properties return

### Test 5: Property Detail
- [ ] Click on any property card
- [ ] Navigate to property detail page
- [ ] See large property image
- [ ] See all property information
- [ ] See contact form in sidebar
- [ ] See mortgage calculator in sidebar

### Test 6: Favorites
- [ ] Click heart icon on a property card
- [ ] Icon fills in (becomes solid)
- [ ] See notification "Added to favorites!"
- [ ] Click heart again
- [ ] Icon empties (becomes outline)
- [ ] See notification "Removed from favorites"

### Test 7: Mortgage Calculator
- [ ] On property detail page
- [ ] Scroll to mortgage calculator
- [ ] Home price pre-filled
- [ ] Adjust down payment to 25%
- [ ] Set interest rate to 7.0%
- [ ] Click "Calculate"
- [ ] See monthly payment estimate

### Test 8: Responsive Design
- [ ] Resize browser to mobile width (< 480px)
- [ ] Layout adjusts to single column
- [ ] Navigation menu adapts
- [ ] Cards stack vertically
- [ ] All features still functional

### Test 9: API Endpoints
- [ ] Test GET all properties
  ```bash
  curl http://localhost:5000/api/properties
  ```

- [ ] Test GET single property
  ```bash
  curl http://localhost:5000/api/properties/1
  ```

- [ ] Test with filters
  ```bash
  curl "http://localhost:5000/api/properties?city=Seattle"
  ```

### Test 10: Database Verification
- [ ] Check properties table
  ```bash
  mysql -u root -p realestate_db -e "SELECT COUNT(*) FROM properties;"
  ```

- [ ] View sample data
  ```bash
  mysql -u root -p realestate_db -e "SELECT id, title, price, city FROM properties LIMIT 5;"
  ```

- [ ] Check favorites table exists
  ```bash
  mysql -u root -p realestate_db -e "SHOW TABLES;"
  ```

## 🐛 Troubleshooting

### Issue: Port 5000 Already in Use
**Solution**: Change port in `app.py`
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Database Connection Error
**Check**:
- [ ] MySQL server is running
  ```bash
  sudo service mysql status
  # or
  systemctl status mysql
  ```
- [ ] Credentials in `.env` are correct
- [ ] Database exists
- [ ] User has proper permissions

**Fix**:
```bash
# Restart MySQL
sudo service mysql restart

# Grant permissions
mysql -u root -p
GRANT ALL PRIVILEGES ON realestate_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Issue: Module Not Found (Flask, etc.)
**Solution**: Reinstall dependencies
```bash
pip3 install -r requirements.txt --upgrade
```

### Issue: No Properties Showing
**Check**:
- [ ] Database initialized (check console on startup)
- [ ] Tables created
- [ ] Sample data inserted

**Fix**: Stop and restart app
```bash
# Stop with Ctrl+C
# Start again
python3 app.py
```

### Issue: Images Not Loading
**Solution**: Images use Unsplash CDN
- Check internet connection
- Verify image URLs in database

### Issue: Favorites Not Saving
**Check**:
- [ ] Browser console for errors (F12)
- [ ] API endpoint responding
- [ ] Database permissions

**Test**:
```bash
curl -X POST http://localhost:5000/api/favorites \
  -H "Content-Type: application/json" \
  -d '{"property_id": 1, "user_email": "test@example.com"}'
```

## 📊 Performance Checks

### Page Load Time
- [ ] Homepage loads in < 2 seconds
- [ ] Property detail loads in < 1 second
- [ ] API responses in < 500ms

### Browser Console
- [ ] No JavaScript errors (F12 → Console)
- [ ] No 404 errors for resources
- [ ] API calls successful

### Network Tab
- [ ] Check API response times (F12 → Network)
- [ ] Verify all resources load
- [ ] Check for optimization opportunities

## 🎉 Success Criteria

Your installation is successful if:

✅ All pre-installation requirements met
✅ All dependencies installed without errors
✅ Database created and initialized
✅ Application starts without errors
✅ Homepage loads and displays properties
✅ Search and filters work correctly
✅ Property detail pages load
✅ Favorites functionality works
✅ Mortgage calculator computes correctly
✅ Responsive design works on mobile
✅ API endpoints respond correctly
✅ No console errors in browser

## 📝 Post-Installation

### Optional Enhancements
- [ ] Add custom properties
  ```bash
  python3 add_property_example.py
  ```

- [ ] Customize colors in `static/css/style.css`
- [ ] Add your logo/branding
- [ ] Configure production settings
- [ ] Set up domain name
- [ ] Enable HTTPS

### Documentation Review
- [ ] Read `README.md` for full documentation
- [ ] Review `FEATURES_GUIDE.md` for features
- [ ] Check `ARCHITECTURE.md` for technical details
- [ ] See `QUICKSTART.md` for quick reference

## 🚀 Production Deployment

Before deploying to production:

- [ ] Set `debug=False` in `app.py`
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up Nginx reverse proxy
- [ ] Configure SSL certificate
- [ ] Set strong database password
- [ ] Enable firewall rules
- [ ] Set up automated backups
- [ ] Configure monitoring
- [ ] Test all functionality on production

## 📞 Support

If you encounter issues not covered here:

1. Check console error messages
2. Review documentation files
3. Verify database connection
4. Check file permissions
5. Ensure all dependencies installed
6. Try test script: `python3 test_app.py`

## 🎓 Learning Resources

After installation:
- Explore the codebase
- Modify sample data
- Customize the design
- Add new features
- Study the API structure
- Experiment with filters

---

**Congratulations on your successful installation!** 🎉

Your RealEstate website is now ready to use!

Visit: **http://localhost:5000**

---

*Last Updated: 2025-10-03*
