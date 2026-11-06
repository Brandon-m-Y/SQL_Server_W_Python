import json
import pandas as pd

TABLE = "dbo.Orders"  # must match the table in create_tables.sql


def read_csv_file(conn, filename, key="OrderID", delete_missing=False):
    """Add a CSV file's new rows to the table and update its changed ones.

    key: the column that identifies each row.
    delete_missing: also delete table rows that aren't in the CSV. Only use this
    when the CSV holds every row, not just new or changed ones.
    """
    df = pd.read_csv(filename)
    cols = list(df.columns)  # must match the table's column names

    # Build the pieces of the SQL from the column names.
    names = ", ".join(cols)                                         # OrderID, OrderDate, ...
    placeholders = ", ".join("?" * len(cols))                       # ?, ?, ...
    updates = ", ".join(f"{c} = s.{c}" for c in cols if c != key)   # OrderDate = s.OrderDate, ...
    values = ", ".join(f"s.{c}" for c in cols)                      # s.OrderID, s.OrderDate, ...

    # For each CSV row (s), look for a table row (t) with the same key.
    # Found: update it. Not found: add it.
    # Running the same file again leaves the table the same.
    sql = f"""
        MERGE INTO {TABLE} AS t
        USING (VALUES ({placeholders})) AS s ({names})
        ON t.{key} = s.{key}
        WHEN MATCHED THEN UPDATE SET {updates}
        WHEN NOT MATCHED THEN INSERT ({names}) VALUES ({values});
    """

    cur = conn.cursor()                       # sends SQL to the database
    cur.executemany(sql, df.values.tolist())  # run it once for each row; fails on an empty CSV

    if delete_missing:
        # Send the CSV's keys as one list and delete table rows whose key isn't in it.
        # OPENJSON turns the list into rows SQL Server can compare against.
        keys = json.dumps(df[key].tolist())
        cur.execute(f"DELETE FROM {TABLE} WHERE {key} NOT IN (SELECT value FROM OPENJSON(?))", keys)

    cur.close()
    return df
