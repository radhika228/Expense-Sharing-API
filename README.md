# Expense Sharing API

A backend application built using Python, FastAPI, and SQLite to manage shared expenses among group members.

## Features

- Create and list users.
- Create groups.
- Add members to groups.
- View group members.
- Add expenses to a group.
- Split expenses equally among group members.
- Calculate balances between group members.
- View group expenses.
- Search expenses by description.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## Project Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd Expense-Sharing-API
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
uvicorn main:app --reload
```

### 7. Open API documentation

Visit:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /users | Create a user |
| GET | /users | List all users |
| POST | /groups | Create a group |
| POST | /groups/{group_id}/members | Add a member |
| GET | /groups/{group_id}/members | List group members |
| POST | /expenses | Add an expense |
| GET | /groups/{group_id}/expenses | List group expenses |
| GET | /groups/{group_id}/balances | Calculate balances |

## Database Design

The application uses SQLite with SQLAlchemy ORM.

Main database tables:

- **Users:** Stores user information.
- **Groups:** Stores group information.
- **Group Members:** Maintains the many-to-many relationship between users and groups.
- **Expenses:** Stores expense details, including amount, description, payer, and group.

## Expense Splitting Logic

Expenses are divided equally among all members of the selected group.

The application calculates each member's share and determines the net balance of every member.

The balance calculation uses integer cents to reduce floating-point precision errors. Any remaining cents are distributed deterministically among group members.

The payer receives credit for the full amount paid, while their own share is included in the equal split.

## Product Enhancement: Expense Search

An optional search parameter has been added to the group expenses endpoint.

Example:

`GET /groups/2/expenses?search=Dinner`

### Problem

In groups with many expenses, finding a particular expense can become difficult.

### Solution

Users can search expenses by description using an optional query parameter.

### Trade-offs

The implementation uses case-insensitive partial matching. It is simple and useful for small datasets. For larger datasets, database indexing or full-text search could improve performance.

## Future Improvements

- Unequal expense splitting.
- Expense settlement functionality.
- User authentication and authorization.
- Automated unit testing.
- Docker support.

## Author

Developed as part of a backend engineering assignment.