import pyodbc
from connect_to_db import build_conn_str
from get_data import read_csv_file
from push_to_db import run_sql_file


# Runs only when you start this file directly (python main.py),
# not when another file imports it.
if __name__ == "__main__":

    conn = None  # stays None if connecting fails, so we know not to close it
    try:
        # autocommit=True saves each change right away, with no separate save step.
        conn = pyodbc.connect(build_conn_str(), autocommit=True)
        run_sql_file(conn, "create_tables.sql")  # create the table
        read_csv_file(conn, "orders.csv")     # fill it with the CSV's rows
        print("Script ran successfully")
    except pyodbc.Error as ex:
        # A database problem: couldn't connect, or SQL Server rejected the SQL.
        # ex holds SQL Server's error message.
        print("Failed")
        print(ex)
    finally:
        # Always close the connection, whether or not the steps above worked.
        if conn:
            conn.close()
