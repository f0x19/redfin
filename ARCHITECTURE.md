# RealEstate Application Architecture

## System Overview

This is a full-stack web application built with Flask (Python) for the backend and vanilla HTML/CSS/JavaScript for the frontend, using MySQL as the database.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   HTML5    │  │    CSS3    │  │ JavaScript │            │
│  │ Templates  │  │   Styles   │  │   Logic    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTP Requests
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Flask Web Server (Python)               │   │
│  │                                                      │   │
│  │  ┌──────────────┐    ┌──────────────────────────┐  │   │
│  │  │   Routes     │    │     API Endpoints        │  │   │
│  │  │   - /        │    │  - /api/properties       │  │   │
│  │  │   - /property│    │  - /api/properties/:id   │  │   │
│  │  │              │    │  - /api/favorites        │  │   │
│  │  └──────────────┘    └──────────────────────────┘  │   │
│  │                                                      │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │        Business Logic & Data Access          │  │   │
│  │  │  - Property filtering and search             │  │   │
│  │  │  - Database connection management            │  │   │
│  │  │  - Data serialization                        │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────┘
                            │ SQL Queries
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATABASE LAYER                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              MySQL Database Server                   │   │
│  │                                                      │   │
│  │  ┌──────────────┐         ┌──────────────┐         │   │
│  │  │ properties   │         │  favorites   │         │   │
│  │  │   table      │◄────────│    table     │         │   │
│  │  └──────────────┘  FK     └──────────────┘         │   │
│  │                                                      │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Database Driver**: mysql-connector-python 8.2.0
- **CORS Handling**: flask-cors 4.0.0
- **Configuration**: python-dotenv 1.0.0

### Frontend
- **Markup**: HTML5 with Jinja2 templating
- **Styling**: CSS3 (Custom, no frameworks)
- **Scripting**: Vanilla JavaScript (ES6+)
- **Icons**: Font Awesome 6.4.0 (CDN)

### Database
- **RDBMS**: MySQL 5.7+ / MariaDB
- **Schema**: Relational with foreign keys

## Component Details

### 1. Flask Application (`app.py`)

**Responsibilities:**
- HTTP request handling
- Routing and view rendering
- API endpoint implementation
- Database connection management
- Data serialization (JSON)

**Key Functions:**
- `get_db_connection()`: Manages MySQL connections
- `init_db()`: Creates tables and sample data
- API routes for CRUD operations on properties
- Template rendering for web pages

### 2. Frontend Templates

#### `templates/index.html`
- Main property listing page
- Search bar and advanced filters
- Grid layout for property cards
- Navigation and footer

#### `templates/property_detail.html`
- Detailed property information
- Image gallery
- Contact form
- Mortgage calculator
- Property specifications

### 3. Static Assets

#### `static/css/style.css`
- Modern, responsive design
- CSS Grid and Flexbox layouts
- Custom CSS variables for theming
- Mobile-first approach
- Smooth animations and transitions

#### `static/js/main.js`
- Property listing logic
- Search and filter functionality
- Favorite management
- API communication
- Dynamic DOM manipulation

#### `static/js/property_detail.js`
- Property detail page logic
- Mortgage calculator
- Contact form handling
- Favorite toggle functionality

## Data Flow

### 1. Property Listing Flow

```
User → Browser → GET / → Flask → Render index.html
                                      ↓
Browser → GET /api/properties → Flask → MySQL Query
                                      ↓
Browser ← JSON Response ← Flask ← Query Results
                                      ↓
Browser → Render Property Cards (JavaScript)
```

### 2. Property Search Flow

```
User Types in Search Box
        ↓
JavaScript Captures Input
        ↓
Build Query Parameters
        ↓
GET /api/properties?search=...&city=...&min_price=...
        ↓
Flask Processes Filters
        ↓
MySQL WHERE Clause Construction
        ↓
Filtered Results Returned
        ↓
JavaScript Re-renders Grid
```

### 3. Property Detail Flow

```
User Clicks Property Card
        ↓
Navigate to /property/{id}
        ↓
Flask Renders property_detail.html
        ↓
JavaScript Loads via /api/properties/{id}
        ↓
MySQL Single Row Query
        ↓
Populate Page with Property Data
```

## Database Schema

### Properties Table
```sql
properties (
    id              PRIMARY KEY AUTO_INCREMENT,
    title           VARCHAR(255),
    description     TEXT,
    price           DECIMAL(12,2),
    address         VARCHAR(255),
    city            VARCHAR(100),
    state           VARCHAR(50),
    zip_code        VARCHAR(20),
    bedrooms        INT,
    bathrooms       DECIMAL(3,1),
    square_feet     INT,
    lot_size        INT,
    year_built      INT,
    property_type   VARCHAR(50),
    listing_type    VARCHAR(20),
    status          VARCHAR(20),
    image_url       TEXT,
    created_at      TIMESTAMP,
    updated_at      TIMESTAMP
)
```

### Favorites Table
```sql
favorites (
    id              PRIMARY KEY AUTO_INCREMENT,
    property_id     INT FOREIGN KEY → properties(id),
    user_email      VARCHAR(255),
    created_at      TIMESTAMP,
    UNIQUE(property_id, user_email)
)
```

## API Endpoints

### Properties API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/properties` | Get all properties with optional filters |
| GET | `/api/properties/<id>` | Get single property details |
| POST | `/api/properties` | Create new property listing |

### Favorites API

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/favorites` | Add property to favorites |
| GET | `/api/favorites/<email>` | Get user's favorites |

## Security Considerations

**Current Implementation:**
- Environment variables for database credentials
- CORS enabled (configure for production)
- SQL injection prevention via parameterized queries

**Production Recommendations:**
- Add user authentication (JWT or sessions)
- Implement rate limiting
- Add CSRF protection
- Use HTTPS only
- Validate and sanitize all inputs
- Implement proper authorization
- Add logging and monitoring

## Scalability Considerations

**Current Architecture:**
- Single Flask process (development server)
- Direct MySQL connections per request

**Production Recommendations:**
1. Use production WSGI server (Gunicorn/uWSGI)
2. Implement connection pooling
3. Add caching layer (Redis)
4. Use CDN for static assets
5. Database replication for read scaling
6. Load balancer for multiple app instances
7. Separate API and web servers

## Development Workflow

```
1. Edit Code
2. Flask Auto-Reload (Debug Mode)
3. Test in Browser
4. Check MySQL Data
5. Iterate
```

## Deployment Architecture

```
Internet
   ↓
[Load Balancer]
   ↓
[Nginx Reverse Proxy]
   ↓
[Gunicorn Workers] ← Flask App Instances
   ↓
[MySQL Primary] ↔ [MySQL Replicas]
   ↓
[Backup System]
```

## Future Enhancements

1. **User Authentication**: Login/Signup system
2. **Image Upload**: Property photo management
3. **Agent Portal**: Separate interface for agents
4. **Advanced Search**: Map-based search, neighborhood data
5. **Notifications**: Email alerts for new listings
6. **Analytics**: Property view tracking
7. **Reviews**: User reviews and ratings
8. **Virtual Tours**: 3D property tours
9. **Messaging**: In-app messaging between buyers and agents
10. **Mobile App**: Native iOS/Android apps

## Monitoring and Maintenance

**Recommended Tools:**
- **Application Monitoring**: New Relic, DataDog
- **Error Tracking**: Sentry
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Database Monitoring**: MySQL Enterprise Monitor
- **Uptime Monitoring**: Pingdom, UptimeRobot

---

This architecture provides a solid foundation for a real estate listing platform with room for growth and enhancement.
