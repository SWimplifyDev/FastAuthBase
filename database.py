from tinydb import TinyDB, Query

db = TinyDB('db.json',sort_keys=True, indent=4, separators=(',', ': '))

speakers_table = db.table('speakers')
users_table = db.table('users')

UserQ = Query()