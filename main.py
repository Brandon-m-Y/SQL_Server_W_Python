"""
Run a .sql file against SQL Server.

Reads connection settings from a .env file, connects with Windows
authentication, and executes every batch in the given .sql file.
"""

# --- Imports ----------------------------------------------------------------
import os                       # read environment variables (os.getenv)
import re                       # regular expressions, used to split the SQL on GO
from pathlib import Path        # object-oriented file paths

import pyodbc                   # ODBC bridge for talking to SQL Server
from dotenv import load_dotenv  # loads KEY=value pairs from a .env file


# --- Configuration ----------------------------------------------------------

# Read the .env file and put its values into os.environ.
# override=True means values in .env replace any variable with the same name
# that's already set (e.g. left over in an open terminal or notebook kernel).
load_dotenv(override=True)

# The folder that holds the .sql files. __file__ is the path of this script and
# .parent is the folder it lives in, so this works no matter which directory
# you run the script from.
SQL_DIR = Path(__file__).parent


def build_conn_str(database=None):
    """Build an ODBC connection string from the .env settings.

    Pass `database` to connect to a specific database (e.g. "master");
    otherwise the DATABASE value from .env is used.
    """
    # ODBC connection strings are KEY=value pairs separated by semicolons.
    # In an f-string, {{ and }} produce literal braces, so {{{x}}} becomes
    # {value}: the braces ODBC needs around driver names that contain spaces.
    return (
        f"DRIVER={{{os.getenv('DRIVER')}}};"
        f"SERVER={os.getenv('SERVER')};"
        # `database or ...` uses the argument if one was passed, else the .env value
        f"DATABASE={database or os.getenv('DATABASE')};"
        # Must be "yes" for Windows authentication (no username/password)
        f"Trusted_Connection={os.getenv('TRUSTED_CONNECTION')};"
    )


def run_sql_file(conn, filename):
    """Execute every batch in a .sql file on an open connection."""
    # Read the whole file into one string. "utf-8-sig" is UTF-8 that also strips
    # the invisible byte-order mark (BOM) SSMS sometimes adds to the start of a
    # file, which would otherwise cause a syntax error on the first statement.
    sql = (SQL_DIR / filename).read_text(encoding="utf-8-sig")

    # GO is a batch separator understood by SSMS and sqlcmd, not by SQL Server
    # itself, so sending it through pyodbc fails. Split the script on any line
    # that contains only GO, and run each piece separately.
    #   ^ and $ with re.MULTILINE -> match the start/end of each line
    #   \s*                       -> allow spaces around GO
    #   re.IGNORECASE             -> also match "go" or "Go"
    batches = re.split(r"^\s*GO\s*$", sql, flags=re.IGNORECASE | re.MULTILINE)

    # A cursor is the object that sends statements to the server.
    cursor = conn.cursor()
    for batch in batches:
        # Skip empty pieces (e.g. the text after a trailing GO)
        if batch.strip():
            cursor.execute(batch)
    cursor.close()


# --- Main -------------------------------------------------------------------

# Start as None so the finally block can tell whether a connection was made.
conn = None
try:
    # Open the connection. autocommit=True makes each statement take effect
    # immediately; without it, changes sit in an open transaction until you
    # call conn.commit(). CREATE DATABASE also refuses to run inside a
    # transaction, so autocommit is required for that.
    conn = pyodbc.connect(build_conn_str(), autocommit=True)
    run_sql_file(conn, "create_db.sql")
    print("Script ran successfully")
except pyodbc.Error as ex:
    # Catches connection failures and errors from the SQL itself;
    # ex holds the SQLSTATE code and SQL Server's error message.
    print("Failed")
    print(ex)
finally:
    # Runs whether the try block succeeded or failed, so the connection
    # is always released.
    if conn:
        conn.close()