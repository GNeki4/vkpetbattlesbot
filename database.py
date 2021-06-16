import sqlite3

conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()

# sql = "DELETE FROM users WHERE id = '161226832'"
# cursor.execute(sql)
# conn.commit()


def create_table():
    cursor.execute('CREATE TABLE users '
                   '(id integer, name text, surname text, nickname text)')


def append(id, name, surname, nickname):
    row = (id, name, surname, nickname)
    sql = """INSERT INTO users (id, name, surname, nickname) VALUES (?, ?, ?, ?);"""
    cursor.execute(sql, row)
    conn.commit()


def update(id, nickname):
    sql = 'Update users set nickname = ? where id = ?'
    data = (nickname, id)
    cursor.execute(sql, data)
    conn.commit()


def get(id):
    sql = 'SELECT nickname FROM users WHERE id=?'
    cursor.execute(sql, (id, ))
    return cursor.fetchall()[0][0]

