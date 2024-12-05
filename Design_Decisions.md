# **Design Decisions**

This document outlines the key design decisions made during the development of the restaurant menu extraction and filtering system. These decisions were made to ensure scalability, usability, and maintainability of the system while leveraging Django and external APIs.

---

## **1. Technology Stack**
### **Backend Framework: Django**
- **Reasoning:** 
  - Django provides a robust ORM for managing relational databases.
  - Built-in features like authentication, admin panel, and form handling simplified development.
  - Its modular structure aligns well with the separation of concerns between the API, database models, and frontend.
- **Alternatives Considered:** Flask or FastAPI were considered but lacked the comprehensive "batteries-included" nature of Django.

### **Database: MySQL**
- **Reasoning:**
  - MySQL was chosen for its reliability, scalability, and extensive community support.
  - Compatibility with Django's ORM and the ability to perform complex SQL queries when needed.
- **Alternatives Considered:** PostgreSQL for advanced data types but decided on MySQL due to familiarity and performance.

### **API Integration: OpenAI**
- **Reasoning:**
  - OpenAI's GPT-4 is capable of parsing unstructured text into structured JSON, which aligns perfectly with the goal of extracting and organizing menu data.
  - The API supports natural language processing, making it an ideal choice for working with complex, imperfectly formatted menu texts.

---

## **2. System Architecture**
### **Layered Approach**
The system follows a layered architecture to separate concerns:
1. **Frontend (Templates):**
   - Uses Django's templating engine to render dynamic pages.
   - Includes filters and structured UI for user interaction.
2. **Backend (Views & Models):**
   - Handles data fetching, filtering logic, and business rules.
   - Integrates with APIs and communicates with the database.
3. **Database:**
   - Stores normalized data including restaurants, menus, food items, dietary restrictions, and relationships between them.

### **RESTful API Integration**
- **Design Choice:** The system integrates a FastAPI service for menu text processing. Django sends raw text extracted from uploaded files to the API, which returns structured JSON.
- **Why FastAPI?**
  - Asynchronous capabilities for faster response times.
  - Lightweight and easy to integrate with Django.

---

## **3. Key Features and Decisions**
### **Menu Parsing with GPT-4 API**
- **Decision:** Use OpenAI's GPT-4 for parsing unstructured menu text into structured JSON.
- **Why?**
  - Handling diverse formats of menus that may vary in structure and quality.
  - Reduces the manual effort required to process menu data.
  
### **Filtering by Dietary Restrictions**
- **Decision:** Allow users to filter menu items based on dietary restrictions.
- **Why?**
  - Enhances usability for specific user needs like vegetarian, gluten-free, etc.
  - Achieved through a join table `FoodItemRestriction` that maps food items to dietary restrictions.

### **Filtering by Restaurant**
- **Decision:** Enable filtering food items by restaurant and grouping results accordingly.
- **Why?**
  - Helps users locate items from specific restaurants.
  - Improves the scalability of the system by allowing restaurant-level queries.

---

## **4. Data Schema Design**
### **Normalization**
- The database schema is normalized to avoid redundancy and ensure maintainability.
- Key tables:
  - **Restaurant:** Stores details about each restaurant.
  - **Menu:** Stores menus linked to restaurants.
  - **MenuItem:** Links food items to specific menus.
  - **FoodItemRestriction:** A many-to-many relationship table for dietary restrictions.
  - **DietaryRestriction:** Defines dietary categories.

### **Relationships**
- **Restaurant ↔ Menu:** One-to-Many.
- **Menu ↔ MenuItem:** One-to-Many.
- **MenuItem ↔ FoodItemRestriction ↔ DietaryRestriction:** Many-to-Many.

---

## **5. User Interface Design**
### **Dynamic Filtering**
- **Decision:** Include filters for dietary restrictions and restaurants.
- **Implementation:**
  - Sidebar for filtering criteria.
  - Results dynamically update without affecting other components of the page.
  - Ensured filters do not clutter the UI and remain accessible.

### **Navigation**
- **Decision:** Use a clean navigation bar with links to:
  - Home
  - Restaurants
  - Upload Menu
  - Reports
