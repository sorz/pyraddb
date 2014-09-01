from . import db


class SqlOnTable(object):
    """Generate SQL queries for a determinate RADIUS attribute table."""

    def __init__(self, table="radcheck", name="username"):
        """Normally, table is one of radcheck, radreply, radgroupcheck
        or radgroupreplay. name is username or groupname.
        """
        self.table = table
        self.name = name


    def select(self):
        return ("SELECT attribute, op, value FROM {0.table} "
                "WHERE {0.name} = %s"
                ).format(self)


    def update(self):
        return ("UPDATE {0.table} SET op = %s, value = %s "
                "WHERE {0.name} = %s AND attribute = %s "
                "LIMIT 1"
                ).format(self)


    def insert(self):
        return ("INSERT INTO {0.table}({0.name}, attribute, op, value) "
                "VALUES (%s, %s, %s, %s)"
                ).format(self)


    def delete(self):
        return ("DELETE FROM {0.table} "
                "WHERE {0.name} = %s AND attribute = %s "
                "LIMIT 1"
                ).format(self)


    def delete_all(self):
        return ("DELETE FROM {0.table} WHERE {0.name} = %s"
                ).format(self)


class Attributes(object):
    def __init__(self, name, sqls):
        self._name = name
        self._sqls = sqls
        cursor = db.cursor()
        cursor.execute(self._sqls.select(), (self._name,))
        self._records = {}
        for attribute, op, value in cursor:
            self._records[attribute] = (op, value)
        cursor.close()

        self.keys = self._records.keys
        self.values = self._records.values


    def __getitem__(self, key):
        return self._records[key]


    def __setitem__(self, key, val):
        if not isinstance(val, tuple):
            raise ValueError("attribute should be a tuple contains "
                    "a operation and a value, not %s." % type(val))
        cursor = db.cursor()
        if key in self._records:
            cursor.execute(self._sqls.update(), 
                    (val[0], val[1], self._name, key))
        else:
            cursor.execute(self._sqls.insert(),
                    (self._name, key, val[0], val[1]))
        cursor.close()
        self._records[key] = val


    def __delitem__(self, key):
        del self._records[key]
        cursor = db.cursor()
        cursor.execute(self._sqls.delete(), (self._name, key))
        cursor.close()


    def __iter__(self):
        return self._records.__iter__()


    def __contains__(self, value):
        self._records.__contains__(value)


    def __repr__(self):
        # TODO: format string.
        return self._records.__repr__()


    def clear(self):
        cursor = db.cursor()
        cursor.execute(self._sqls.delete_all(), (self._name, ))
        cursor.close()
        self._records.clear()


