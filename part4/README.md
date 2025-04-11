# 🏨 HBNB Part 4 - Simple Web Client

## 📋 Overview
This part of the HBNB project focuses on front-end development using HTML5, CSS3, and JavaScript ES6. You'll be creating an interactive user interface that connects with the back-end services developed in previous parts of the project.

## 🎯 Objectives
- Develop a user-friendly interface following provided design specifications
- Implement client-side functionality to interact with the back-end API
- Ensure secure and efficient data handling using JavaScript
- Apply modern web development practices to create a dynamic web application

## 🧠 Learning Goals
- Understand and apply HTML5, CSS3, and JavaScript ES6 in a real-world project
- Learn to interact with back-end services using AJAX/Fetch API
- Implement authentication mechanisms and manage user sessions
- Use client-side scripting to enhance user experience without page reloads

## ✅ Tasks

### 🎨 Task 0: Design
**Complete the visual foundation of your application!**

Create beautiful and functional pages following the provided specifications:
- ✨ Login Form - Your gateway to the application
- 🏢 List of Places - An attractive showcase of available locations
- 🔍 Place Details - In-depth information about each location
- ⭐ Add Review Form - Allow users to share their experiences

Requirements include proper header with logo, responsive footer, and intuitive navigation elements. Remember, all pages must pass W3C validation!

### 🔐 Task 1: Login
**Secure your application with user authentication!**

Build a robust login system that:
- 🔄 Communicates with your API using AJAX requests
- 🔑 Securely stores JWT tokens in cookies
- ↪️ Smoothly redirects users after successful login
- ⚠️ Provides clear feedback when login attempts fail

This foundation ensures only authorized users can access protected features.

### 🏠 Task 2: Index (List of Places)
**Create an engaging showcase of available places!**

Develop a dynamic main page that:
- 📊 Fetches and displays place data from your API
- 💰 Allows users to filter places by price without page reloads
- 👤 Intelligently shows or hides the login link based on authentication status
- 🃏 Presents each place as an attractive card with key information

This page serves as the central hub of your application.

### 🔎 Task 3: Place Details
**Reveal the complete story of each location!**

Implement a comprehensive details view that:
- 📝 Fetches complete place information using the place ID
- 📋 Displays rich content including descriptions, amenities, and user reviews
- 💬 Provides authenticated users access to the review submission form
- 🖼️ Presents information in a clear, organized layout

This page turns browsing into an immersive experience.

### ✍️ Task 4: Add Review Form
**Let users share their experiences!**

Create an intuitive review submission system that:
- 🛡️ Restricts access to authenticated users only
- 🔄 Redirects unauthorized visitors to the index page
- 📤 Submits review data to the API endpoint
- 📢 Provides clear feedback on submission success or failure

This feature builds community engagement around your listings.

## ⚠️ CORS Configuration Note
When testing your client against your API, you'll likely encounter Cross-Origin Resource Sharing (CORS) errors. You'll need to modify your API code to allow your client to fetch data from the API.

## 📚 Resources
- HTML5 Documentation
- CSS3 Documentation
- JavaScript ES6 Features
- Fetch API
- Responsive Web Design Basics
- Handling Cookies in JavaScript
- Client-Side Form Validation
- DOM Manipulation
- FormData API

## 📁 Repository
- GitHub repository: holbertonschool-hbnb
- Directory: part4