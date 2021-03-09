import sqlite3 as sql

from itertools import cycle


def xor(message, key):
    return bytes(a ^ b for a, b in zip(message, cycle(key)))


def pass_cipher(password):
    key1 = b'this_is_key'
    key2 = b'also_here_another'
    result = xor(password.encode(), key1)

    return xor(result, key2)


con = sql.connect('user_list.db')
cur = con.cursor()
cur.execute("""INSERT INTO 'user_list' VALUES (?, ?, ?, ?);""",
            ('Admin', pass_cipher('1-2-3Admin3-2-1'), 'Admin', True))
con.commit()
cur.close()

# Login - Admin
# Password - 1-2-3Admin3-2-1
