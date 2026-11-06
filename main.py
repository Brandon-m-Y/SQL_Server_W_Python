import pyodbc
from connect_to_db import build_conn_str
from get_data import read_csv_file
from push_to_db import run_sql_file


# Runs only when you start this file directly (python main.py),
# not when another file imports it.
if __name__ == "__main__":

    conn = None  # stays None if connecting fails, so we know not to close it
    try:
        # autocommit=False holds every change until commit(), so a failed run changes nothing.
        conn = pyodbc.connect(build_conn_str(), autocommit=False)
        run_sql_file(conn, "create_tables.sql")  # create the table if it's missing

        # Make the table match the CSV. delete_missing=True because orders.csv holds
        # every order; use False for a file of only new or changed rows.
        read_csv_file(conn, "orders.csv", delete_missing=True)

        conn.commit()  # save everything at once
        print("Script ran successfully")
    except pyodbc.Error as ex:
        # A database problem: couldn't connect, or SQL Server rejected the SQL.
        # ex holds SQL Server's error message.
        print("Failed")
        print(ex)
    finally:
        # Always close the connection. Anything not committed is undone.
        if conn:
            conn.close()
