pyraddb
=======

A small tool to play with FreeRADIUS database, easy to manage users and groups.


```
from pyraddb import db
from pyraddb import User, Group

db.connect_mysql(user='radius', password='123', 
        database='radius')

alice = User("Alice")
alice.check['Cleartext-Password'] = (':=', 'passme')
alice.group['Friends'] = 10  # Priority is 10.

friends = Group("Friends")
friends.reply['Fall-Through'] = ('=', 'Yes')

friends.allusers()
>>> ('Alice', 'Bob')

db.commit()
```

Only support MySQL with default schema.

Under alpha development, use at your own risk.
