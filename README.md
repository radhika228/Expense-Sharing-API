# Expense Sharing API

A backend application built using Python, FastAPI, SQLAlchemy, and SQLite to manage shared expenses among group members and calculate balances.

The application allows users to create groups, add members, record shared expenses, split expenses equally, and calculate who owes whom.

## 1. Features

- Create and list users.
- Create expense groups.
- Add users to groups.
- View group members.
- Record expenses within a group.
- Split expenses equally among group members.
- Calculate balances between group members.
- View expense history.
- Search expenses by description.
- Validate expense amounts and group membership.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| FastAPI | REST API framework |
| SQLAlchemy | ORM for database operations |
| SQLite | Relational database |
| Pydantic | Request data validation |
| Uvicorn | ASGI server |

## 3. Architecture Overview

The application follows a simple layered backend architecture.

- **API Layer:** FastAPI handles incoming HTTP requests and returns responses.
- **Validation Layer:** Pydantic validates incoming request data.
- **Database Layer:** SQLAlchemy ORM manages database operations.
- **Database:** SQLite stores users, groups, memberships, and expenses.

### Application Flow

Client Request → FastAPI Endpoint → Request Validation → SQLAlchemy ORM → SQLite Database → API Response

## 4. Database Design

The application uses SQLite with SQLAlchemy ORM.

### Tables

**Users**
- id (Primary Key)
- name

Stores user information.

**Groups**
- id (Primary Key)
- name

Stores expense group information.

**Group Members**
- group_id (Foreign Key)
- user_id (Foreign Key)

Maintains a many-to-many relationship between users and groups. A user can belong to multiple groups, and a group can contain multiple users.

**Expenses**
- id (Primary Key)
- group_id (Foreign Key)
- paid_by (Foreign Key referencing Users)
- amount
- description

Stores expense details, including the group, payer, amount, and description.

### Relationships

- One user can belong to multiple groups.
- One group can contain multiple users.
- One group can have multiple expenses.
- Each expense belongs to one group.
- Each expense has one payer.

## 5. Project Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/radhika228/Expense-Sharing-API.git
```

### Step 2: Navigate to the Project Directory

```bash
cd Expense-Sharing-API
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
uvicorn main:app --reload
```

### Step 7: Open API Documentation

Visit:

http://127.0.0.1:8000/docs

## 6. API Documentation

The application provides REST APIs for user management, group management, expense management, and balance calculation.

| Method | Endpoint | Description |
|---|---|---|
| POST | /users | Create a new user |
| GET | /users | List all users |
| POST | /groups | Create a new group |
| POST | /groups/{group_id}/members | Add a user to a group |
| GET | /groups/{group_id}/members | List group members |
| POST | /expenses | Add a new expense |
| GET | /groups/{group_id}/expenses | List group expenses |
| GET | /groups/{group_id}/balances | Calculate group balances |

Interactive API documentation is available through Swagger UI at `/docs` when the application is running.

## 7. Expense Splitting and Balance Calculation

Expenses are divided equally among all members of the selected group.

### Example

Consider a group with three members:

- Mohit
- Rahul
- Ankit

Mohit pays ₹1200 for dinner.

Total expense = ₹1200

Number of members = 3

Each member's share = ₹1200 / 3 = ₹400

Therefore:

- Rahul owes Mohit ₹400.
- Ankit owes Mohit ₹400.
- Mohit's own share is ₹400.

The balance calculation considers each member's total contribution and individual share to determine net balances.

The implementation uses integer cents to reduce floating-point precision errors. Any remaining cents are distributed deterministically among group members.

## 8. Assumptions Made

- Every expense is split equally among all members of the selected group.
- Only existing users can be added to groups.
- The payer must be a member of the selected group.
- Expense amounts must be greater than zero.
- The payer should not owe themselves.
- All expenses are recorded in INR.
- Group membership is considered at the time of balance calculation.

## 9. Design Decisions

- **FastAPI:** Selected because it provides a simple and efficient way to build REST APIs with automatic documentation.
- **SQLite:** Selected because it is lightweight and suitable for a small backend assignment.
- **SQLAlchemy ORM:** Used to simplify database operations and model relationships.
- **Many-to-Many Relationship:** Used between users and groups to support multiple group memberships.
- **Decimal Amounts:** Used for storing financial values to avoid floating-point precision issues.
- **Equal Expense Splitting:** Implemented using integer cents to ensure accurate distribution.
- **Expense Search:** Added an optional search parameter to help users find expenses by description.

## 10. Product Enhancement: Expense Search

### Problem

In groups with multiple expenses, finding a particular expense can become difficult.

### Solution

An optional search parameter has been added to the group expenses API.

Example:

`GET /groups/2/expenses?search=Dinner`

Users can search expenses using a description keyword.

### Design Decisions

- Search is implemented using an optional query parameter.
- Case-insensitive partial matching is supported.
- Existing expense listing functionality remains available when no search keyword is provided.

### Trade-offs

The implementation is simple and suitable for small datasets. For larger datasets, database indexing or full-text search could improve performance.

## 11. Future Improvements

With more development time, the application can be improved by:

- Implementing user authentication and authorization.
- Supporting unequal expense splitting.
- Adding expense settlement functionality.
- Writing automated unit and integration tests.
- Adding expense categories and monthly spending analytics.
- Migrating SQLite to PostgreSQL for production use.
- Adding Docker support.
- Improving API error handling and validation.

## 12. Running Tests

The application can be tested through the interactive Swagger UI.

Start the server:

```bash
uvicorn main:app --reload
```

Then open:

http://127.0.0.1:8000/docs

Use the available endpoints to create users, groups, members, and expenses, and verify the balance calculations.

## 13. Author

Developed as part of the Decentro SDE Intern technical assignment.