# 🏨 HBNB - Holberton AirBnB Clone

## 📋 Project Overview
HBNB is a comprehensive AirBnB clone application built using Python and Flask. This project implements a RESTful API backend with a web frontend that allows users to register, manage properties, leave reviews, and associate amenities with places.

---

## 🏗️ Architecture
The application follows a three-layered architecture:

- **🖥️ Presentation Layer**: API endpoints and web interface  
- **🧠 Business Logic Layer**: Core models and business rules  
- **💾 Persistence Layer**: Database interactions and storage  

---

## ✨ Features

- 👤 User registration and authentication with JWT  
- 🏠 Property (place) listing and management  
- ⭐ Review system for properties  
- 🛋️ Amenity management and association with places  
- 👑 Admin functionality for property management  
- 📱 Responsive web interface  

---

## 📁 Directory Structure

.
├── app/ # Main application package
│ ├── init.py # App initialization
│ ├── extensions.py # Flask extensions
│ ├── api/ # API endpoints
│ │ ├── v1/ # API version 1
│ │ ├── amenities.py # Amenities endpoints
│ │ ├── auth.py # Authentication endpoints
│ │ ├── places.py # Places endpoints
│ │ ├── protector.py # JWT protection middleware
│ │ ├── reviews.py # Reviews endpoints
│ │ └── users.py # Users endpoints
│ ├── models/ # Data models
│ │ ├── amenity.py # Amenity model
│ │ ├── base_model.py # Base model with common functionality
│ │ ├── place.py # Place model
│ │ ├── review.py # Review model
│ │ └── user.py # User model
│ ├── persistence/ # Data storage layer
│ │ ├── amenity_repository.py # Amenity storage operations
│ │ ├── place_repository.py # Place storage operations
│ │ ├── repository.py # Base repository interface
│ │ ├── review_repository.py # Review storage operations
│ │ └── user_repository.py # User storage operations
│ └── services/ # Business logic services
│ └── facade.py # Facade pattern implementation
├── config.py # Application configuration
├── run.py # Application entry point
├── static/ # Static assets (CSS, JS, images)
├── templates/ # HTML templates for the web interface
├── tests/ # Test suite for the application
├── ER_diag.md # Entity-relationship diagram documentation
├── requirements.txt # Project dependencies list
└── setup.sql # Database setup script

---

## 🚀 Installation and Setup

### 📋 Prerequisites

- 🐍 Python 3.10+  
- 🔄 Virtual environment (recommended)  
- 🗄️ SQLite (for development) or MySQL (for production)  

### 📝 Setup Steps

1. Clone the repository:
    ```
    git clone <repository-url>
    cd hbnb
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Configure the database:
    ```
    python setup.sql  # For SQLite (development)

    # For MySQL (production):
    # Configure MySQL credentials in config.py and run:
    mysql -u username -p < setup.sql
    ```

5. Run the application:
    ```
    python run.py
    ```

---

## 🌐 API Endpoints

### 🔐 Authentication

- `POST /api/v1/auth/login` - User login  
- `POST /api/v1/auth/register` - User registration  

### 👤 Users

- `GET /api/v1/users` - List all users  
- `GET /api/v1/users/<id>` - Get user details  
- `PUT /api/v1/users/<id>` - Update user information  

### 🏠 Places

- `GET /api/v1/places` - List all places  
- `GET /api/v1/places/<id>` - Get place details  
- `POST /api/v1/places` - Create a new place  
- `PUT /api/v1/places/<id>` - Update place information  

### ⭐ Reviews

- `GET /api/v1/places/<place_id>/reviews` - List reviews for a place  
- `POST /api/v1/places/<place_id>/reviews` - Add a review to a place  
- `PUT /api/v1/reviews/<id>` - Update a review  
- `DELETE /api/v1/reviews/<id>` - Delete a review  

### 🛋️ Amenities

- `GET /api/v1/amenities` - List all amenities  
- `GET /api/v1/amenities/<id>` - Get amenity details  
- `POST /api/v1/amenities` - Create a new amenity  
- `PUT /api/v1/amenities/<id>` - Update amenity information  

---

## 🔒 Authentication Details

The application uses JWT (JSON Web Tokens) for authentication. Protected endpoints require a valid token in the Authorization header:

Authorization: Bearer <your-jwt-token>

text

To obtain a token, use the login endpoint with valid credentials.

---

## 🧪 Testing

Run the test suite with pytest:

pytest

text

To run specific tests:

pytest tests/test_user.py # Run user tests only.
pytest tests/test_place.py # Run place tests only.

text

---

## 🗄️ Database Schema

The application uses SQLAlchemy ORM with the following main entities:

- 👤 **User**: Stores user information and credentials  
- 🏠 **Place**: Represents properties with location and details  
- ⭐ **Review**: Contains reviews for places  
- 🛋️ **Amenity**: Represents features available at places  

See `ER_diag.md` for a detailed entity-relationship diagram.

---

## 🖥️ Web Interface

The application includes a simple web interface accessible at the root URL:

| URL                | Description                  |
|--------------------|------------------------------|
| `/`                | Homepage with places listing |
| `/login`           | User login page             |
| `/place/<id>`      | Place details page          |
| `/add_review/<id>` | Add review form             |

---

## 📈 Project Evolution

This project has evolved through multiple phases:

1. **📝 Architecture design and documentation**  
2. **🧠 Business logic and API implementation**  
3. **🔐 Authentication, authorization, and database integration**  
4. **🎨 Web interface development**

---

## 🤝 Contributing

1. Fork the repository.  
2. Create a feature branch:
    ```
    git checkout -b feature/amazing-feature
    ```
3. Commit your changes:
    ```
    git commit -m 'Add amazing feature'
    ```
4. Push to the branch:
    ```
    git push origin feature/amazing-feature 
    ```
5. Open a Pull Request.

---

## 📜 License

This project is for educational purposes as part of the Holberton School curriculum.

---

## 🙏 Acknowledgements

Special thanks to:

- 🏫 Holberton School for the project structure and requirements.  
- 🌐 Flask and SQLAlchemy communities for their excellent documentation.
