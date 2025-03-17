# HBnB Project

## Overview
HBnB (Holberton Bed and Breakfast) is a platform for property owners to list their accommodations and for travelers to book and review these places. This implementation uses a Flask backend with SQLAlchemy for database persistence, following clean architecture principles with repository pattern.

## Features
- User authentication with JWT tokens
- User registration with secure password hashing
- Role-based access control (regular users and administrators)
- Property listing management
- Review system for properties
- Database persistence with SQLAlchemy

## Architecture
The application follows a clean architecture approach with distinct layers:
- **Models Layer**: Business entities (User, Place, Review, Amenity)
- **Repository Layer**: Data persistence abstraction
- **Service Layer**: Business logic facade
- **API Layer**: RESTful endpoints

### Repository Pattern
- Initially implemented with in-memory storage
- Transitioned to SQLAlchemy-based database persistence
- Common interface ensures consistency between implementations

## Installation and Setup

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
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## Getting Started

### Initialize the Database
```bash
flask shell
>>> from app import db
>>> db.create_all()
```

### Running the Application
```bash
flask run
```

The API will be available at `http://127.0.0.1:5000/`

## API Endpoints

### Authentication
- `POST /api/v1/auth/login`: Authenticate user and receive JWT token

### Users
- `POST /api/v1/users/`: Create a new user (admin only)
- `GET /api/v1/users/<user_id>`: Get user details
- `PUT /api/v1/users/<user_id>`: Update user details (owner or admin only)

### Places
- `GET /api/v1/places/`: List all places (public)
- `GET /api/v1/places/<place_id>`: Get place details (public)
- `POST /api/v1/places/`: Create a new place (authenticated users)
- `PUT /api/v1/places/<place_id>`: Update place details (owner or admin only)

### Reviews
- `POST /api/v1/reviews/`: Create a new review (authenticated users)
- `PUT /api/v1/reviews/<review_id>`: Update review (owner or admin only)
- `DELETE /api/v1/reviews/<review_id>`: Delete review (owner or admin only)

### Amenities
- `POST /api/v1/amenities/`: Add a new amenity (admin only)
- `PUT /api/v1/amenities/<amenity_id>`: Update amenity (admin only)

## Security Features
- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- Ownership validation for resource modification