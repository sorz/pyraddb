from .attributes import SqlOnTable, Attributes
from . import db


class UserChecks(Attributes):
    def __init__(self, username):
        super().__init__(username, SqlOnTable('radcheck', 'username'))


class UserRepies(Attributes):
    def __init__(self, username):
        super().__init__(username, SqlOnTable('radreply', 'username'))


class GroupChecks(Attributes):
    def __init__(self, groupname):
        super().__init__(groupname, SqlOnTable('radgroupcheck', 'groupname'))


class GroupRepies(Attributes):
    def __init__(self, groupname):
        super().__init__(groupname, SqlOnTable('radgroupreply', 'groupname'))


class UserGroups(object):
    def __init__(self, username):
        self._username = username
        query = ("SELECT groupname, priority FROM radusergroup "
                "WHERE username = %s")
        cursor = db.cursor()
        cursor.execute(query, (self._username, ))
        self._records = {}
        for groupname, priority in cursor:
            self._records[groupname] = priority
        cursor.close()

        self.keys = self._records.keys
        self.values = self._records.values


    def __getitem__(self, key):
        return self._records[key]


    def __setitem__(self, key, val):
        cursor = db.cursor()
        if key in self._records:
            query = ("UPDATE radusergroup SET priority = %s "
                    "WHERE username = %s AND groupname = %s AND priority = %s "
                    "LIMIT 1")
            cursor.execute(query, 
                    (val, self._username, key, self._records[key]))
        else:
            query = ("INSERT INTO radusergroup(username, groupname, priority) "
                    "VALUES (%s, %s, %s)")
            cursor.execute(query,
                    (self._username, key, val))
        cursor.close()
        self._records[key] = val


    def __delitem__(self, key):
        # TODO: Check if key exist.
        cursor = db.cursor()
        query = ("DELETE FROM radusergroup "
                "WHERE username = %s AND groupname = %s AND priority = %s "
                "LIMIT 1")
        cursor.execute(query, (self._username, key, self._records[key]))
        cursor.close()
        del self._records[key]


    def __iter__(self):
        return self._records.__iter__()


    def __contains__(self, value):
        self._records.__contains__(value)


    def __repr__(self):
        return self._records.__repr__()


    def clear(self):
        cursor = db.cursor()
        query = ("DELETE FROM radusergroup WHERE username = %s")
        cursor.execute(query, (self._username, ))
        cursor.close()
        self._records.clear()


def get_users_by_group(groupname):
    cursor = db.cursor()
    query = ("SELECT username FROM radusergroup WHERE groupname = %s")
    cursor.execute(query, (groupname, ))
    users = [i[0] for i in cursor]
    cursor.close()
    return users


def delete_usergroup_by_group(groupname):
    cursor = db.cursor()
    query = ("DELETE FROM radusergroup WHERE groupname = %s")
    cursor.execute(query, (groupname, ))
    cursor.close()

