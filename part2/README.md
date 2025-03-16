# HBnB API - Part 2

## Overview
HBnB (Holberton Bed & Breakfast) API is a RESTful web service that manages property rentals, user accounts, reviews, and amenities. This project implements a robust backend using Flask, SQLAlchemy, and JWT authentication.

## Key Features
1. **Authentication & Authorization**
   - JWT-based authentication
   - Role-based access control (Admin/User)
   - Secure password hashing with bcrypt

2. **Data Models**
   - User: Account management and authentication
   - Place: Property listings with location and pricing
   - Review: User reviews for properties
   - Amenity: Property features and facilities

3. **Architecture**
   - Repository Pattern for data access
   - Facade Pattern for business logic
   - SQLAlchemy ORM for database operations

4. **API Endpoints**
   - `/api/v1/auth`: Authentication operations
   - `/api/v1/users`: User management
   - `/api/v1/places`: Property operations
   - `/api/v1/reviews`: Review management
   - `/api/v1/amenities`: Amenity operations

5. **Database Structure**
   - SQLite for development
   - Proper relationships (One-to-Many, Many-to-Many)
   - Data validation and integrity constraints

## Getting Started
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

## API Documentation
API documentation is available at `/api/v1/` when running the application.

## Database Schema
The application uses SQLAlchemy models with the following relationships:
- User -> Places (One-to-Many)
- User -> Reviews (One-to-Many)
- Place -> Reviews (One-to-Many)
- Place <-> Amenities (Many-to-Many)

## Diagramme


## Conclusion
This project demonstrates a well-structured API implementation using modern Python web development practices. It provides a solid foundation for property rental management with proper security measures and efficient data handling.

## Authors
- Dimitri Jaille
- Mattieu Mouroux



