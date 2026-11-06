"""Load the settings in .env and build the details needed to connect to SQL Server."""

import os                       # reads settings
from pathlib import Path        # works with file and folder locations
from dotenv import load_dotenv  # loads the .env file

# Load the settings in .env. override=True means .env wins over any setting
# with the same name that's already set in your terminal.
load_dotenv(override=True)

# The folder this file is in. The .sql files are looked for here,
# no matter which folder you run the script from.
SQL_DIR = Path(__file__).parent


def build_conn_str(database=None):
    """Return the connection text SQL Server needs, built from the .env settings.

    Pass a database name to use it instead of the one in .env.
    """
    # Each setting is written as NAME=value; and joined into one line.
    # The triple braces put { } around the driver name, which it needs
    # because the name has spaces.
    return (
        f"DRIVER={{{os.getenv('DRIVER')}}};"
        f"SERVER={os.getenv('SERVER')};"
        f"DATABASE={database or os.getenv('DATABASE')};"
        # "yes" logs in with your Windows account, so no password is needed.
        f"Trusted_Connection={os.getenv('TRUSTED_CONNECTION')};"
    )
