from . import db
from . import usergroup


class User(object):
    """Create, modify or view a user by specified username.

    user.check (or user.reply): a dict-like object for attributes.
    The key is attribute name, value is a tuple includes the operations
    and the actual value.

    e.g user.check['Cleartext-Password'] = (':=', 'passme')
        (set password for this user)
    
    Use `del user.check['key']` to delete a attribute.

    user.group: a dict-like obect for all groups this user belongs.
    The key is groupname, value is the priority.
    """
    def __init__(self, username):
        """username may be the new for create a group."""
        self._username = username
        self.check = usergroup.UserChecks(username)
        self.reply = usergroup.UserRepies(username)
        self.group = usergroup.UserGroups(username)


    def delete(self):
        """Delete this user from check, reply and group."""
        self.check.clear()
        self.reply.clear()
        self.group.clear()


    def __repr__(self):
        return "User (%s)" % self._username


    def __str__(self):
        return self._username


class Group(object):
    """Create, modify or view a group by specified groupname.

    group.check, group.reply: the same as User's.
    """
    def __init__(self, groupname):
        """groupname may be the new for create a group."""
        self._groupname = groupname
        self.check = usergroup.GroupChecks(groupname)
        self.reply = usergroup.GroupRepies(groupname)


    def delete(self, not_touch_usergroup=False):
        """Delete all related records on check, reply and usergroup tables.

        Note that no user will belongs this group after delete
        unless not_touch_usergroup = True.
        """
        if not not_touch_usergroup:
            usergroup.delete_usergroup_by_group(self._groupname)
        self.check.clear()
        self.reply.clear()


    def allusers(self):
        """Return a list includes all users belong this group."""
        return usergroup.get_users_by_group(self._groupname)


    def __repr__(self):
        return "Group (%s)" % self._groupname


    def __str__(self):
        return self._groupname

