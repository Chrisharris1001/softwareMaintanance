import sqlite3

# Define the database path in one place so it is easy to change later
DB_PATH = r'ims.db'

def execute_query(query, params=()):
    """
    Executes an INSERT, UPDATE, or DELETE query.
    Handles the connection, commit, and closing automatically.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute(query, params)
        con.commit()
    except Exception as e:
        print(f"Database Execution Error: {e}")
        raise e
    finally:
        con.close()

def fetch_query(query, params=()):
    """
    Executes a SELECT query and returns the fetched rows.
    Handles the connection and closing automatically.
    """
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    try:
        cur.execute(query, params)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Database Fetch Error: {e}")
        raise e
    finally:
        con.close()