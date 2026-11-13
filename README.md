# Expense Sharing API

A backend application built with FastAPI to manage users, groups, shared expenses, expense search, and net settlements.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic
- Python-dotenv
- Pytest

## Features

- Create and list users.
- Create groups and add members.
- Create and manage group expenses.
- Categorize expenses.
- Equal expense splitting.
- Validate expense inputs.
- Search expenses by description.
- Get autocomplete suggestions for expense descriptions.
- Calculate net balances and settlement suggestions.
- Environment-based database configuration.

## Project Structure

```text
Expense_Sharing/
│
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── group.py
│   │   └── expense.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── group.py
│   │   └── expense.py
│   │
│   ├── routers/
│   │   ├── users.py
│   │   ├── groups.py
│   │   └── expenses.py
│   │
│   ├── services/
│   │   ├── expense_service.py
│   │   └── balance_service.py
│   │
│   ├── database.py
│   └── main.py
│
├── tests/
├── expense.db
├── migrate_db.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository.

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Configure the database.

The application uses SQLite by default. The database URL can also be configured through the `DATABASE_URL` environment variable.

Example:

```env
DATABASE_URL=sqlite:///./expense.db
```

6. Run the application from the project root:

```bash
uvicorn app.main:app --reload
```

7. Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| POST | `/users` | Create a user |
| GET | `/users` | List users |
| POST | `/groups` | Create a group |
| POST | `/groups/{group_id}/members` | Add a group member |
| GET | `/groups/{group_id}/members` | List group members |
| POST | `/expenses` | Create an expense |
| GET | `/groups/{group_id}/expenses` | List group expenses |
| GET | `/groups/{group_id}/expenses/suggestions` | Get expense suggestions |
| GET | `/groups/{group_id}/balances` | Calculate group balances |

## Expense Search

The group expenses endpoint supports searching by description using the optional `search` query parameter.

Example:

```text
/groups/1/expenses?search=dinner
```

Search is case-insensitive.

## Expense Suggestions

The suggestions endpoint returns matching expense descriptions.

Example:

```text
/groups/1/expenses/suggestions?q=din
```

It returns up to 10 distinct matching descriptions.

## Database Design

- `users`: Stores user information.
- `groups`: Stores group information.
- `group_members`: Implements the many-to-many relationship between users and groups.
- `expenses`: Stores expense details, including amount, category, split type, group, and payer.

## Expense Calculation

- Expenses are currently split equally among group members.
- Amounts are converted into integer minor currency units (paise) to avoid floating-point calculation errors.
- Remaining paise are distributed deterministically.
- Net balances are converted into settlement suggestions.

**Note:** Percentage and custom split types are not currently supported. Equal splitting is the implemented functionality.

## Validation and Error Handling

- Validates expense amounts and descriptions.
- Checks whether the group and payer exist.
- Ensures that the payer belongs to the group.
- Rejects unsupported split types.

## Database Migration

The `migrate_db.py` script checks whether the `category` and `split_type` columns exist in the expenses table and adds them if necessary.

Run it using:

```bash
python migrate_db.py
```

## Run Tests

Run the automated tests using:

```bash
python -m pytest -v
```

## Future Improvements

- Percentage and custom expense splitting.
- Expense settlement recording.
- Authentication and authorization.
- Additional automated API tests.
- Pagination.

## Docker Setup

The application can also be run using Docker.

### Build Docker Image

```bash
docker build -t expense-sharing-api .
```

### Run Docker Container

```bash
docker run -d --name expense-api -p 8002:8000 expense-sharing-api
```

### Access API

Open the following URL in your browser:

http://127.0.0.1:8002/docs

### Check Running Containers

```bash
docker ps
```

### Stop Container

```bash
docker stop expense-api
```

### Remove Container

```bash
docker rm expense-api
```