# 🏨 HBnB Project - Part 3: Enhanced Backend 🚀

## 📋 Overview

Welcome to Part 3 of the HBnB Project! This phase focuses on extending the backend with:

- 🔐 User authentication & authorization using JWT
- 💾 Database integration with SQLAlchemy
- 🗄️ Persistence layer transition (SQLite for development, MySQL for production)
- 📊 Database schema design and visualization

## 🎯 Key Objectives

- Implement secure user authentication with JWT tokens
- Replace in-memory storage with persistent database solutions
- Design proper database relationships between entities
- Create role-based access control for regular users and administrators

## ✨ Featured Tasks

### 🔧 Task 0: Application Factory Configuration
**Configure your Flask application factory to work with different environments**
- Update `create_app()` to accept configuration parameters
- Implement environment-specific settings

### 🔑 Task 1: Secure Password Management
**Enhance the User model with password hashing**
- Implement bcrypt for secure password storage
- Update registration endpoints to handle passwords
- Ensure passwords are never returned in API responses

### 🔒 Task 2: JWT Authentication
**Set up secure token-based authentication**
- Implement login functionality with JWT tokens
- Configure protected endpoints requiring authentication
- Handle token generation, validation, and expiration

### 👤 Task 3: User Access Control
**Restrict endpoint access to authenticated users**
- Secure creation and modification of places and reviews
- Implement ownership validation (users can only modify their own content)
- Maintain public access for non-protected endpoints

### 👑 Task 4: Administrator Privileges
**Implement role-based access control for admins**
- Allow admins to create and modify user accounts
- Give admins unrestricted access to modify any content
- Implement the `is_admin` flag in the JWT token

### 💿 Task 5: SQLAlchemy Repository
**Replace in-memory storage with database persistence**
- Create `SQLAlchemyRepository` class implementing the repository interface
- Refactor the Facade to use the new repository pattern
- Prepare the foundation for ORM integration

### 🧩 Task 6: User Entity Mapping
**Map the User model to the database**
- Extend BaseModel with SQLAlchemy functionality
- Implement User-specific database operations
- Ensure password hashing remains functional with ORM

### 🏢 Task 7: Entity Mapping
**Map Place, Review, and Amenity models to the database**
- Define core attributes for all entities
- Update repositories for database interactions
- Implement CRUD operations for each entity

### 🔗 Task 8: Entity Relationships
**Define connections between database entities**
- Implement one-to-many relationships (User-Place, Place-Review)
- Create many-to-many relationships (Place-Amenity)
- Configure proper foreign keys and constraints

### 📜 Task 9: SQL Scripts
**Create database initialization scripts**
- Generate table creation SQL statements
- Write scripts to populate initial data
- Insert admin user and basic amenities

### 📊 Task 10: Database Diagrams
**Visualize the database schema**
- Create Entity-Relationship diagrams using Mermaid.js
- Document all tables and their relationships
- Export diagrams for project documentation

## 🛠️ Technologies Used

- **Flask**: Web framework
- **Flask-JWT-Extended**: Authentication
- **SQLAlchemy**: ORM for database interactions
- **SQLite**: Development database
- **MySQL**: Production database
- **Bcrypt**: Password hashing
- **Mermaid.js**: Database schema visualization

## 📚 Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Mermaid.js Documentation](https://mermaid-js.github.io/mermaid/)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## 🚀 Getting Started

1. Clone the repository
2. Set up your virtual environment
3. Install dependencies
4. Configure your database settings
5. Run the application and start implementing the tasks

## 📝 Notes

This part of the project builds on previous components, transitioning from a prototype to a production-ready application with secure authentication and persistent storage.
