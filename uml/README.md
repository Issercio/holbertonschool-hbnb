# 🏠 HBnB Evolution Project 🏠

## 📋 Project Overview

Welcome to the **HBnB Evolution** project! This project involves creating a comprehensive technical documentation for an AirBnB-like application. The documentation will serve as the foundation for the development of the application, helping to understand the overall architecture, business logic design, and system interactions.

## 🎯 Project Objective

Create detailed technical documentation for HBnB Evolution - a simplified version of an AirBnB-like application that allows users to:
- 👤 Register and manage user profiles
- 🏘️ List and manage properties
- ⭐ Leave reviews for places
- 🛋️ Associate amenities with places

## 🧩 Application Components

### Entity Management
1. **User Entity**
   - Attributes: first name, last name, email, password, admin status
   - Operations: register, update profile, delete

2. **Place Entity**
   - Attributes: title, description, price, location (latitude/longitude)
   - Relations: owner (user), amenities
   - Operations: create, update, delete, list

3. **Review Entity**
   - Attributes: rating, comment
   - Relations: place, user
   - Operations: create, update, delete, list by place

4. **Amenity Entity**
   - Attributes: name, description
   - Operations: create, update, delete, list

### Architecture
The application follows a **three-layered architecture**:
- 🖥️ **Presentation Layer**: Services and API
- 🧠 **Business Logic Layer**: Models and core logic
- 💾 **Persistence Layer**: Database storage and retrieval

## ✅ Project Tasks

### Task 0: High-Level Package Diagram ✨
**Objective**: Create a package diagram illustrating the three-layer architecture and communication via facade pattern.

**Requirements**:
- Show three layers (Presentation, Business Logic, Persistence)
- Illustrate communication pathways between layers
- Apply facade pattern
- Include explanatory notes

### Task 1: Detailed Class Diagram for Business Logic Layer 📊
**Objective**: Design a class diagram for the Business Logic layer focusing on key entities.

**Requirements**:
- Include User, Place, Review, and Amenity entities
- Define attributes, methods, and relationships
- Include UUIDs and creation/update dates
- Use proper UML notation
- Include explanatory notes

### Task 2: Sequence Diagrams for API Calls 🔄
**Objective**: Develop sequence diagrams for API calls showing layer interactions.

**Requirements**:
- Create diagrams for:
  - User registration
  - Place creation
  - Review submission
  - Fetching a list of places
- Show step-by-step flow between layers
- Include explanatory notes

### Task 3: Documentation Compilation 📚
**Objective**: Compile all diagrams and notes into a comprehensive technical document.

**Requirements**:
- Include introduction to the project
- Organize sections for:
  - High-level architecture
  - Business logic layer details
  - API interaction flows
- Add explanatory notes for each diagram
- Ensure professional formatting and clarity

## 📝 Key Requirements

- All entities must have unique IDs
- Creation and update datetimes should be recorded for audit purposes
- All diagrams must use UML notation
- Documentation must clearly show interactions between layers

## 🛠️ Helpful Resources

### UML Basics
- [OOP - Introduction to UML](https://example.com/uml-intro)

### Package Diagrams
- [UML Package Diagram Overview](https://example.com/package-diagrams)
- [UML Package Diagrams Guide](https://example.com/package-guide)

### Class Diagrams
- [UML Class Diagram Tutorial](https://example.com/class-diagrams)
- [How to Draw UML Class Diagrams](https://example.com/draw-class-diagrams)

### Sequence Diagrams
- [UML Sequence Diagram Tutorial](https://example.com/sequence-diagrams)
- [Understanding Sequence Diagrams](https://example.com/sequence-understanding)

### Diagram Tools
- [Mermaid.js Documentation](https://mermaid-js.github.io/mermaid/)
- [draw.io](https://www.draw.io/)

## 🏁 Expected Outcome

By the end of this project, you will have created a complete set of technical documentation that provides a clear blueprint for the HBnB Evolution application. This documentation will guide implementation and ensure a solid understanding of the application's design and architecture.

## 🚀 Getting Started

1. Review the architecture requirements and business rules
2. Start with the high-level package diagram
3. Progress to the detailed class diagram
4. Create sequence diagrams for key API interactions
5. Compile everything into a comprehensive document

Good luck! 🍀
