import sqlite3
import functools
import operator
import random

__connection = None


def get_connection():
    global __connection
    if __connection is None:
        # Подключение к датабазе
        __connection = sqlite3.connect('dat.db', check_same_thread=False)
    return __connection


def init_db(force):
    # Создание курсора
    conn = get_connection()
    curr = conn.cursor()

    # Дропнуть таблицы если force True
    if force:
        tables = ('user_message', 'Clients', 'Orders', "Supplies", "Codes", "Schedule", "ordered_supplies")
        tabless = ('Codes', 'ordered_supplies')
        for table in tabless:
            sql = 'DROP TABLE IF EXISTS ' + table
            curr.execute(sql)
    # Создание таблиц
    curr.execute('''
        CREATE TABLE IF NOT EXISTS ordered_supplies (
            id                     INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id               INTEGER NOT NULL,
            product_id             INTEGER NOT NULL,
            amount                 INTEGER NOT NULL
        )
    ''')

    curr.execute('''
           CREATE TABLE IF NOT EXISTS Clients (
               idClients     INTEGER PRIMARY KEY AUTOINCREMENT,
               Name          TEXT NOT NULL,
               Surname       TEXT NOT NULL,
               Address       TEXT NOT NULL,
               Chat_id       INTEGER NOT NULL,
               Status        TEXT NOT NULL
           )
       ''')

    curr.execute('''
               CREATE TABLE IF NOT EXISTS Orders (
                   Chat_id        INTEGER NOT NULL,
                   address        TEXT NOT NULL,
                   phone_number   INTEGER NOT NULL,
                   Notes          TEXT NOT NULL,
                   Cost           INTEGER NOT NULL
               )
           ''')

    curr.execute('''
                   CREATE TABLE IF NOT EXISTS Supplies (
                       product_id        INTEGER PRIMARY KEY,
                       Name              TEXT NOT NULL,
                       Amount            INTEGER NOT NULL,
                       Price             INTEGER NOT NULL 
                   )
               ''')

    curr.execute('''
                       CREATE TABLE IF NOT EXISTS Codes (
                           code        INTEGER NOT NULL
                       )
                   ''')

    curr.execute('''
                        CREATE TABLE IF NOT EXISTS Schedule (
                            time        INTEGER NOT NULL,
                            day         INTEGER NOT NULL,
                            month       INTEGER NOT NULL,
                            year        INTEGER NOT NULL
                               
                           )
                       ''')

    curr.execute('''
                            CREATE TABLE IF NOT EXISTS Choise (
                                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                                choise    TEXT NOT NULL
                               )
                           ''')
    conn.commit()


def add_to_Clients(Name: str, Surname: str, Address: str, Chat_id: int, Status: str):
    conn = get_connection()
    cur = conn.cursor()
    quer = 'INSERT INTO Clients (Name, Surname, Address, Chat_id, Status) VALUES(?, ?, ?, ?,? )'
    cur.execute(quer, (Name, Surname, Address, Chat_id, Status))
    conn.commit()


def add_to_Choice(choise: str):
    conn = get_connection()
    cur = conn.cursor()
    quer = 'INSERT INTO Choise (choise) VALUES(?)'
    cur.execute(quer, (choise,))
    conn.commit()


def drop_choice():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Choise")
    conn.commit()


def get_choise():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT choise FROM Choise")
    rows = cur.fetchall()
    return rows


def get_ids():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Chat_id FROM Clients")
    rows = cur.fetchall()
    return rows


def get_name(code: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = "SELECT Name FROM Clients WHERE Chat_id = " + str(code)
    cur.execute(quer)
    rows = cur.fetchall()
    return rows


def add_to_Orders(Chat_id: int, address: str, phone_number: int, Notes: str, Cost: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = 'INSERT INTO Orders (Chat_id, address, phone_number, Notes, Cost) VALUES(?, ?, ?, ?, ?)'
    cur.execute(quer, (Chat_id, address, phone_number, Notes, Cost))
    conn.commit()


def add_to_Supplies(product_id: int, Name: int, Amount: int, Price: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = 'INSERT INTO Supplies (product_id, Name, Amount, Price) VALUES(?, ?, ?, ? )'
    cur.execute(quer, (product_id, Name, Amount, Price))
    conn.commit()


def add_to_ordered_supplies(order_id: int, product_id: int, amount: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = 'INSERT INTO ordered_supplies (order_id, product_id, amount) VALUES(?, ?, ? )'
    cur.execute(quer, (order_id, product_id, amount))
    conn.commit()


def add_to_codes(code: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = 'INSERT INTO Codes VALUES(?)'
    cur.execute(quer, (code,))
    conn.commit()


def get_sup():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Name FROM Supplies")
    rows = cur.fetchall()
    return rows


def all_username(code: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = "SELECT EXISTS(SELECT * FROM codes WHERE code = " + str(code)
    cur.execute(quer)
    rows = cur.fetchall()
    qer = functools.reduce(operator.add, (rows[0]))
    return qer


def gen_token():
    token = random.randint(1000000, 9999999)
    add_to_codes(token)


def get_rand():
    token = random.randint(1000000, 9999999)
    return token


def if_token_exists(token: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = "SELECT EXISTS(SELECT 1 FROM Codes WHERE code=" + str(token) + ")"

    cur.execute(quer)
    rows = cur.fetchall()
    return rows[0][0]


def chat_id_name(chid: int):
    conn = get_connection()
    cur = conn.cursor()
    quer = "SELECT EXISTS(SELECT 1 FROM Clients WHERE Chat_id=" + str(chid) + ")"

    cur.execute(quer)
    rows = cur.fetchall()
    return rows[0][0]


def choise_check(choise):
    conn = get_connection()
    cur = conn.cursor()
    # quer = "SELECT EXISTS(SELECT 1 FROM Supplies WHERE Name=" + str(choise) + ")"
    quer = "SELECT EXISTS(SELECT * FROM Supplies WHERE Supplies.Name=" + choise + ");"
    cur.execute(quer)
    rows = cur.fetchall()
    return rows[0][0]


def list_messages(user_id: int, limit: int = 10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM user_message WHERE user_id = ? ORDER BY id DESC LIMIT ? ", (user_id, limit))
    rows = cur.fetchall()
    return rows


if __name__ == '__main__':
    init_db(force=False)
    # # add_to_Clients(3,'Vova','Gavrysh','Gerove 4',12345)
    #  print(if_token_exists("1241234"))
    # print(get_ids())
    # print(get_names())
    #  print(chat_id_name(1382175006))
    # print(get_name(1382175006) )
    # print(get_sup())
    # print(get_choise())

    # print(if_token_exists(123))
