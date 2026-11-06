# Python to SQL Server

Creates a table in SQL Server from a `.sql` file, then fills it with rows from a CSV file.

## Files

| File | What it does |
|---|---|
| `main.py` | Connects, creates the table, and loads the CSV. This is the one you run. |
| `connect_to_db.py` | Reads your settings from `.env` and builds the connection details. |
| `push_to_db.py` | Runs a `.sql` file against the database. |
| `get_data.py` | Reads a CSV file and adds its rows to the table. |
| `create_tables.sql` | Describes the table to create. |

## Setup

1. Install the Python packages:
   ```
   pip install pyodbc python-dotenv pandas
   ```
2. Install Microsoft's **ODBC Driver 17 for SQL Server** if you don't already have it. It's what lets Python reach SQL Server.
3. Copy `.env.example` to `.env` and fill it in:
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
- The table name in `get_data.py` must match the one in `create_tables.sql`.
- The table must not already exist. To run again, delete it first in SSMS (for example, `DROP TABLE dbo.table1;`).

## Run

From this folder:

```
python main.py
```

It prints `Script ran successfully`, or `Failed` followed by SQL Server's error message.
