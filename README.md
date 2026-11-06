# Python to SQL Server

Creates a table in SQL Server from a `.sql` file, then keeps it in step with a CSV file: new rows are added, changed rows are updated, and rows missing from the CSV can be deleted. It's safe to run as often as you like.

## Files

| File | What it does |
|---|---|
| `main.py` | Connects, creates the table if needed, and loads the CSV. This is the one you run. |
| `connect_to_db.py` | Reads your settings from `.env` and builds the connection details. |
| `push_to_db.py` | Runs a `.sql` file against the database. |
| `get_data.py` | Adds, updates, and optionally deletes rows so the table matches a CSV file. |
| `create_tables.sql` | Describes the table, and creates it only if it doesn't exist. |

## Setup

1. Install the Python packages:
   ```
   pip install pyodbc python-dotenv pandas
   ```
2. Install Microsoft's **ODBC Driver 17 for SQL Server** if you don't already have it. It's what lets Python reach SQL Server.
3. Use SQL Server 2016 or newer.
4. Copy `.env.example` to `.env` and fill it in:
   ```
   DRIVER=ODBC Driver 17 for SQL Server
   SERVER=localhost
   DATABASE=YourDatabase
   TRUSTED_CONNECTION=yes
   ```
   - `SERVER` is the name you connect to in SSMS, such as `localhost` or `localhost\SQLEXPRESS`.
   - `TRUSTED_CONNECTION=yes` logs in with your Windows account, so no password is needed.

## Before you run it

- Put your CSV in this folder and put its name in `main.py`.
- The CSV's column headers must match the table's column names.
- `TABLE` in `get_data.py` must match the table in `create_tables.sql`.
- `key` is the column that identifies each row (`OrderID` by default). Each value must be unique.
- `delete_missing=True` in `main.py` deletes table rows that aren't in the CSV. Set it to `False` if your CSV only has new or changed rows.

## Run

From this folder:

```
python main.py
```

It prints `Script ran successfully`, or `Failed` followed by SQL Server's error message. A failed run changes nothing in the database.
