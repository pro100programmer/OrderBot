import sqlite3
import functools
import operator
import random

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('dat.db')
    return __connection


def init_db(force: bool = False):
    conn = get_connection()

    c = conn.cursor()

    # TODO : создать при необходимости

    if force:
        c.execute('DROP TABLE IF EXISTS reg_codes')
    c.execute('''
        CREATE TABLE IF NOT EXISTS reg_codes (
            id               INTEGER PRIMARY KEY,
            code          INTEGER NOT NULL,  
        )
    ''')
    conn.commit()


def add_code(chat_id: int, code: int):
    conn = get_connection()
    c = conn.cursor()
    print(conn)
    c.execute('INSERT INTO reg_codes (code, chat) VALUES (?, ?)', (code, chat_id))
    conn.commit()


def convertTuple(tup):
    str = functools.reduce(operator.add, (tup))
    return str


def gen_code():
    code = random.randint(100000, 999999)
    return code





if __name__ == '__main__':
    init_db()
    add_code(0, 1)
    assign_to_code(1, 1)
