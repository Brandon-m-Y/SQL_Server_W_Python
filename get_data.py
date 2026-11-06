import pandas as pd

def read_csv_file(conn, filename):
    """Read a CSV file, add each of its rows to the table, and return the data read."""

    df = pd.read_csv(filename)

    # Build the insert from the CSV's column names, which must match the table's:
    #   INSERT INTO dbo.Orders (OrderID, OrderDate, Amount) VALUES (?, ?, ?)
    # Each ? is filled in with a value from the row.
    cols = ", ".join(df.columns)
    placeholders = ", ".join("?" * len(df.columns))
    sql = f"INSERT INTO dbo.Orders ({cols}) VALUES ({placeholders})"

    # Run the insert once for each row.
    cur = conn.cursor()  # sends SQL to the database
    cur.executemany(sql, df.values.tolist())
    cur.close()
    return df
