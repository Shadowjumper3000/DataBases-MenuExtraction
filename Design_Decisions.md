## **Design Decisions**

### **1. Technology Stack**
#### **Backend Framework: Django**
- **Why Django?**
  - Robust ORM simplifies database management and querying.
  - Includes built-in tools for authentication, admin panel, and form handling.
  - Promotes modularity, allowing clear separation of API, database, and frontend.

#### **Database: MySQL**
- **Why MySQL?**
  - Reliable, scalable, and widely supported.
  - Efficient performance for complex queries and large datasets.
  - Seamless integration with Django ORM.

#### **AI Integration: OpenAI**
- **Why GPT-4?**
  - Handles diverse and unstructured menu formats with high accuracy.
  - Produces structured JSON output for seamless database insertion.

---

### **2. System Architecture**
#### **Layered Approach**
- **Frontend:** Django templates dynamically render pages and provide filters.
- **Backend:** Handles database operations, API integration, and user interactions.
- **Database:** Stores structured menu data, dietary restrictions, and relationships.

#### **RESTful API Integration**
- **FastAPI:** Processes text from PDFs and integrates with GPT-4.
  - **Why FastAPI?**
    - Lightweight and asynchronous, ensuring faster processing.
    - Handles JSON conversion for unstructured text efficiently.

---

### **3. Database Design**
#### **Normalization**
- Designed in **3NF** to reduce redundancy and improve maintainability.
- Key tables include:
  - **Restaurant:** Stores restaurant metadata.
  - **Menu:** Links to restaurants and contains menu metadata.
  - **MenuSection:** Categorizes menu items (e.g., appetizers, entrees).
  - **MenuItem:** Stores individual food items and pricing.
  - **DietaryRestriction:** Lists dietary categories like vegan, gluten-free.
  - **FoodItemRestriction:** Manages many-to-many relationships between items and restrictions.
  - **ProcessingLog:** Tracks the status and errors in the ETL pipeline.

#### **Relationships**
- **Restaurant ↔ Menu:** One-to-Many.
- **Menu ↔ MenuSection ↔ MenuItem:** One-to-Many.
- **MenuItem ↔ FoodItemRestriction ↔ DietaryRestriction:** Many-to-Many.

#### **Index Strategy**
- Indexed fields for:
  - **Restaurant names**: Frequent searches.
  - **Menu item names**: Filtering and sorting.
  - **Dietary restrictions**: Optimized query performance.

---

### **4. ETL Process**
#### **PDF Text Extraction**
- Extracts raw text using libraries like `PyPDF2` or `pdfplumber`.
- Handles unstructured data with varying formats.

#### **AI Integration**
- Sends extracted text to GPT-4 via FastAPI.
- Converts unstructured text into structured JSON.

#### **Data Validation**
- Ensures completeness and correctness before database insertion:
  - Validates field values (e.g., numerical prices).
  - Checks for missing or duplicate entries.

#### **Error Handling and Logging**
- **ProcessingLog** table tracks ETL pipeline activities and errors.

---

### **5. Query Design**
#### **Retrieve Menu Information**
- Fetches complete menu details, including items, sections, and dietary restrictions.

#### **Filter Items by Dietary Restrictions**
- Joins `FoodItemRestriction` and `DietaryRestriction` to fetch matching menu items.

#### **Track Processing Status**
- Queries `ProcessingLog` for status updates and error details.

#### **Generate Reports**
- Summarizes menu prices, item counts, and restaurant activity.

#### **Handle Menu Updates**
- Supports versioning and historical tracking of menu changes.

---

### **6. User Interface Design**
#### **Dynamic Filtering**
- Sidebar filters for:
  - Dietary restrictions.
  - Restaurant-specific food items.
- Results dynamically update without disrupting the layout.

#### **Navigation**
- Clean navigation bar with links to:
  - Home
  - Restaurants
  - Upload Menu
  - Reports
