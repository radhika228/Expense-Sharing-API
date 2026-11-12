# Expense Sharing API

A backend application for managing users, groups, shared expenses, and net settlements.

## Tech stack
- Python
- FastAPI
- SQLAlchemy ORM
- SQLite
- Pydantic

## Project structure
- `app/models/`: SQLAlchemy database models
- `app/schemas/`: Pydantic request schemas and validation
- `app/routers/`: HTTP endpoints
- `app/services/`: business logic
- `app/database.py`: database engine, session factory, and dependency
- `tests/`: automated tests

## Setup
1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the API from the project root:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Open Swagger documentation at `http://127.0.0.1:8000/docs`.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Health/welcome message |
| POST | `/users` | Create a user |
| GET | `/users` | List users |
| POST | `/groups` | Create a group |
| POST | `/groups/{group_id}/members` | Add a group member |
| GET | `/groups/{group_id}/members` | List group members |
| POST | `/expenses` | Create an expense |
| GET | `/groups/{group_id}/expenses` | List group expenses; optional `search` query |
| GET | `/groups/{group_id}/balances` | Calculate settlement balances |

## Database design
- `users`: user records.
- `groups`: group records.
- `group_members`: association table implementing the many-to-many relationship between users and groups.
- `expenses`: expense records linked to a group and the user who paid.

## Expense calculation
Each expense is split equally among the group's members. Amounts are converted to integer minor currency units (paise) before calculations to avoid floating-point arithmetic. Any remainder is distributed deterministically in member-ID order. Net balances are then matched into settlement transactions.

## Product enhancement: expense search
The group expenses endpoint accepts an optional `search` query parameter and performs case-insensitive matching against the expense description.

Example: `/groups/1/expenses?search=dinner`

## Design decisions and assumptions
- SQLite is used for simple local setup.
- All group members share each expense equally.
- Only a member of the group can be recorded as the payer.
- The balance endpoint returns net settlement suggestions; it does not transfer money.
- Authentication, unequal splits, settlement recording, migrations, pagination, and broader automated API tests are future improvements.

## Run tests
```bash
pytest
```
