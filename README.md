# HBnB - Holberton Bed and Breakfast API

## 📋 Overview
HBnB (Holberton Bed and Breakfast) is a platform for property owners to list their accommodations and for travelers to book and review these places. This implementation uses a Flask backend with SQLAlchemy for database persistence, following clean architecture principles with repository pattern.

## 🏗️ Project Structure
```
.
├── README.md
├── app/
│   ├── __init__.py                # App initialization and configuration
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/                    # API endpoints
│   │       ├── __init__.py
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── extensions.py              # Flask extensions
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   ├── amenity.py
│   │   ├── association_tables.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/               # Data storage
│   │   ├── __init__.py
│   │   ├── amenity_repository.py
│   │   ├── place_repository.py
│   │   ├── repository.py
│   │   ├── review_repository.py
│   │   ├── sqlalchemy_repository.py
│   │   └── user_repository.py
│   └── services/                  # Business logic
│       ├── __init__.py
│       ├── facade.py
│       └── test.py
├── config.py                      # Configuration settings
├── img/                           # Images and diagrams
│   └── Diagram.png
├── init_db.py                     # Database initialization script
├── instance/                      # Instance data
│   └── development.db
├── migrations/                    # Database migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       └── 19dca831a264_initial_migration.py
├── requirements.txt               # Project dependencies
├── run.py                         # Application entry point
├── sql/                           # SQL scripts
│   ├── create_tables.sql
│   ├── insert_initial_data.sql
│   ├── test_queries.sql
│   └── verify_db.sql
└── tests/                         # Tests
    ├── report_HBNB_API.md
    ├── test_API.sh
    ├── test_amenities.py
    ├── test_curl_commands.sh
    ├── test_facade.py
    ├── test_places.py
    ├── test_reviews.py
    └── test_users.py
```

## ✨ Features
- User authentication with JWT tokens
- User registration with secure password hashing
- Role-based access control (regular users and administrators)
- Property listing management
- Review system for properties
- Database persistence with SQLAlchemy

## 🏛️ Architecture
The application follows a clean architecture approach with distinct layers:
- **Models Layer**: Business entities (User, Place, Review, Amenity)
- **Repository Layer**: Data persistence abstraction
- **Service Layer**: Business logic facade
- **API Layer**: RESTful endpoints

### Repository Pattern
- Implements data persistence abstraction
- Uses SQLAlchemy for database persistence
- Common interface ensures consistency between implementations

## 🚀 Installation and Setup

### Prerequisites
- Python 3.8+
- pip

### Installation
1. Clone the repository
```bash
git clone <repository-url>
cd hbnb
```

2. Create and activate a virtual environment
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Configuration
The application uses different configuration profiles:
- Development (default)
- Production
- Testing

Configuration is managed through the `config.py` file with options for:
- Secret key for JWT tokens
- Database URI
- Debug mode
- SQLAlchemy settings

To change environment:
```bash
export FLASK_ENV=development  # or testing/production
```

### Database Initialization
```bash
python init_db.py
```
or
```bash
flask shell
>>> from app import db
>>> db.create_all()
```

### Running the Application
```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/login`: Authenticate user and receive JWT token

### Users
- `POST /api/v1/users/`: Create a new user (admin only)
- `GET /api/v1/users/`: List all users
- `GET /api/v1/users/<user_id>`: Get user details
- `PUT /api/v1/users/<user_id>`: Update user details (owner or admin only)

### Places
- `POST /api/v1/places/`: Create a new place
- `GET /api/v1/places/`: List all places
- `GET /api/v1/places/<id>`: Get specific place details
- `PUT /api/v1/places/<id>`: Update place (owner or admin only)

### Reviews
- `POST /api/v1/reviews/`: Create a new review (authenticated users)
- `GET /api/v1/reviews/`: List all reviews
- `GET /api/v1/reviews/<id>`: Get specific review details
- `PUT /api/v1/reviews/<id>`: Update review (owner or admin only)
- `DELETE /api/v1/reviews/<id>`: Delete review (owner or admin only)

### Amenities
- `POST /api/v1/amenities/`: Add a new amenity (admin only)
- `GET /api/v1/amenities/`: List all amenities
- `GET /api/v1/amenities/<id>`: Get specific amenity details
- `PUT /api/v1/amenities/<id>`: Update amenity (admin only)

## 📊 Response Formats

### Success Response
```json
{
    "id": "uuid",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    ...resource specific fields...
}
```

### Error Response
```json
{
    "error": "Error message"
}
```

## 🔒 Security Features
- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Ownership validation for resource modification

## 🗃️ Data Models and Relationships

### User
- Attributes: `id`, `first_name`, `last_name`, `email`, `password`, `is_admin`
- Relationships: 
  - A user can create multiple places (one-to-many)
  - A user can write multiple reviews (one-to-many)

### Place
- Attributes: `id`, `title`, `description`, `price`, `latitude`, `longitude`, `owner_id`
- Relationships:
  - A place belongs to a single user (many-to-one)
  - A place can have multiple reviews (one-to-many)
  - A place can have multiple amenities (many-to-many)

### Review
- Attributes: `id`, `text`, `rating`, `user_id`, `place_id`
- Relationships:
  - A review is written by a single user (many-to-one)
  - A review is associated with a single place (many-to-one)

### Amenity
- Attributes: `id`, `name`
- Relationships:
  - An amenity can be associated with multiple places (many-to-many)

## 📝 Model Validation Rules

### User Model
- First name and last name cannot be empty
- Valid email format required

### Place Model
- Title cannot be empty
- Price must be positive
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180

### Review Model
- Text cannot be empty
- Rating must be between 1 and 5
- Valid user_id and place_id required

### Amenity Model
- Name cannot be empty
- Name must be between 1 and 50 characters

## 🧪 Tests

### Running Tests
```bash
python -m unittest discover tests
```

or

```bash
bash tests/test_API.sh
```

### Tests with curl
```bash
bash tests/test_curl_commands.sh
```

### Test Examples

#### User Creation Test
```python
def test_create_user(self):
    response = self.client.post('/api/v1/users/', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com"
    })
    self.assertEqual(response.status_code, 201)
```

#### Place Creation Test
```python
def test_create_place(self):
    response = self.client.post('/api/v1/places/', json={
        "title": "Mountain View",
        "price": 150.0,
        "latitude": 37.7749,
        "longitude": -122.4194
    })
    self.assertEqual(response.status_code, 201)
```

## 📚 Documentation

### API Documentation
API documentation is automatically generated using Swagger/OpenAPI.
Access `http://127.0.0.1:5000/api/docs` to view the interactive documentation.

### Code Documentation
The code is documented with docstrings conforming to PEP 257 standards.

## 🔄 SQL Scripts

### Available Scripts
The following SQL scripts are available in the `sql/` directory:

- `create_tables.sql`: Creates all tables with their constraints
- `insert_initial_data.sql`: Inserts the initial data
- `test_queries.sql`: Test queries to verify the database
- `verify_db.sql`: Database verifications

To execute the SQL scripts:
```bash
psql -U <user> -d <database> -f sql/create_tables.sql
psql -U <user> -d <database> -f sql/insert_initial_data.sql
```

## 🤝 Contribution
1. Create a branch for your feature (`git checkout -b feature/my-feature`)
2. Commit your changes (`git commit -m 'Add my feature'`)
3. Push to the branch (`git push origin feature/my-feature`)
4. Open a Pull Request

### Coding Standards
- PEP 8 compliance for Python code style
- Unit tests for all new features
- Documentation of functions and classes with docstrings

## 🚢 Deployment

### Deployment with Docker
```bash
docker build -t hbnb .
docker run -p 5000:5000 hbnb
```

### Production Deployment
For production deployment, configure environment variables:
```bash
export FLASK_ENV=production
export DATABASE_URL=<your-db-url>
export SECRET_KEY=<your-secret-key>
```

Use a WSGI server such as Gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
```