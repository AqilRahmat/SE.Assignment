#NOTE : This part is only for table creation. DO NOT alter this
import sqlite3

#connect to the database
def connect():
    conn = sqlite3.connect("CeriaPay.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#Create the tables
def create_table():
    conn = connect()
    c = conn.cursor()

    #admin table
    c.execute('''
    CREATE TABLE IF NOT EXISTS administrator (
    admin_id TEXT PRIMARY KEY,
    admin_name TEXT NOT NULL,
    admin_contactnum TEXT NOT NULL,
    admin_username TEXT NOT NULL,
    admin_password TEXT NOT NULL
    )''')

    #accountant table
    c.execute('''
    CREATE TABLE IF NOT EXISTS accountant (
    accountant_id TEXT PRIMARY KEY,
    accountant_name TEXT NOT NULL,
    accountant_contactnum TEXT NOT NULL,
    accountant_username TEXT NOT NULL,
    accountant_password TEXT NOT NULL
    )''')

    # feerecord
    c.execute('''
        CREATE TABLE IF NOT EXISTS feerecord  (
        feerecord_id TEXT PRIMARY KEY,
        feerecord_duedate DATE NOT NULL,
        feerecord_amount REAL NOT NULL,
        feerecord_status TEXT NOT NULL,
        feerecord_timecreated DATETIME NOT NULL
        )''')

    #parent table
    c.execute('''
    CREATE TABLE IF NOT EXISTS parent (
    parent_id TEXT PRIMARY KEY,
    feerecord_id INTEGER,
    parent_name TEXT NOT NULL,
    parent_contactnum TEXT NOT NULL,
    parent_username TEXT NOT NULL,
    parent_password TEXT NOT NULL,
    FOREIGN KEY (feerecord_id) REFERENCES feerecord (feerecord_id) ON DELETE SET NULL ON UPDATE CASCADE
    )''')

    conn.commit()
    conn.close()