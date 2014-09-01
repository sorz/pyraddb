import mysql.connector


_conn = None

def connect_mysql(**kwargs):
    """Sets database connection parameters for the whole pragram.
    Should be called at first.

    See all arguments on http://dev.mysql.com/doc/connector-python/en/
                         connector-python-connectargs.html
    """
    global _conn
    if _conn is not None:
        _conn.close()
        _conn = None
    _conn = mysql.connector.connect(**kwargs)


def cursor():
    """Return the cursor of database."""
    return _conn.cursor()


def commit():
    """Save all modification.
    
    This function must be called when modify completed.
    """
    _conn.commit()


def rollback():
    """Undo all data change."""
    _conn.rollback()

