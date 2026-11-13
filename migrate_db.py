from sqlalchemy import inspect, text
from app.database import engine


def migrate_database():
    inspector = inspect(engine)

    if "expenses" not in inspector.get_table_names():
        print("Expenses table does not exist.")
        return

    existing_columns = {
        column["name"]
        for column in inspector.get_columns("expenses")
    }

    with engine.begin() as connection:

        if "category" not in existing_columns:
            connection.execute(
                text(
                    "ALTER TABLE expenses "
                    "ADD COLUMN category VARCHAR(50) NOT NULL DEFAULT 'Other'"
                )
            )
            print("Category column added.")

        if "split_type" not in existing_columns:
            connection.execute(
                text(
                    "ALTER TABLE expenses "
                    "ADD COLUMN split_type VARCHAR(20) NOT NULL DEFAULT 'equal'"
                )
            )
            print("Split type column added.")

    print("Database migration completed!")


if __name__ == "__main__":
    migrate_database()