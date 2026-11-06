import re
from connect_to_db import SQL_DIR


def run_sql_file(conn, filename):
    """Run everything in a .sql file."""
    # Read the file. "utf-8-sig" drops a hidden marker that some editors, like
    # SSMS, put at the start of a file. SQL Server would reject it as an error.
    sql = (SQL_DIR / filename).read_text(encoding="utf-8-sig")

    # A line that says GO splits a .sql file into parts. SSMS understands GO,
    # but SQL Server doesn't, so split the file on any line that is only GO
    # (any capitalization, extra spaces allowed) and run each part on its own.
    batches = re.split(r"^\s*GO\s*$", sql, flags=re.IGNORECASE | re.MULTILINE)

    cursor = conn.cursor()  # sends SQL to the database
    for batch in batches:
        if batch.strip():  # skip empty parts, like the one after a final GO
            cursor.execute(batch)
    cursor.close()
