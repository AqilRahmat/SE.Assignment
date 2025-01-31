#NOTE : This part is only for table creation and functio to insert data into tables. DO NOT use  this file to insert items directly
import cmath
import sqlite3

#connect to the database
def connect():
    conn = sqlite3.connect("CeriaPay.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

#function to remove an entry
#note that this will remove the entire entry (name, id etc)
#to update the entry use the update_entry function
def remove_entry(table, column, condition):
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    query = "DELETE FROM {} WHERE {} = ?".format(table, column)
    c.execute(query, (condition,))

    conn.commit()
    conn.close()

#update the entry
def update_entry(table, column, value, condition_column, condition_value):
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    # Format the query to update the entry
    query = "UPDATE {} SET {} = ? WHERE {} = ?".format(table, column, condition_column)

    # Execute the update query
    c.execute(query, (value, condition_value))

    conn.commit()
    conn.close()

#Insert into parent table
def insert_into_parentdatabase(parentid, feeid, name, contact, user, password):
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    c.execute('''
    INSERT INTO parent (parent_id, feerecord_id, parent_name, parent_contactnum, parent_username, parent_password)
    VALUES(?,?,?,?,?,?)
    ''', (parentid, feeid, name, contact, user, password))

    conn.commit()
    conn.close()

#insert into admin (this is for admin only)
def insert_into_admindatabase(id, name, num, user, password):
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    c.execute('''
    INSERT INTO admin (admin_id, admin_name, admin_contactnum, admin_username, admin_password)
    VALUES(?,?,?,?,?)
    ''', (id, name, num, user, password))

    conn.commit()
    conn.close()

#insert into accountant table (this is for admin only)
def insert_into_accountantdatabase(id, name, num, user, password):
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    c.execute('''
    INSERT INTO accountant (accountant_id, accountant_name, accountant_contactnum, accountant_username, accountant_password)
    VALUES(?,?,?,?,?)
    ''', (id, name, num, user, password))

    conn.commit()
    conn.close()

#insert into feerecord table
def insert_into_feerecorddatabase(id, amount, status):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    current_time = datetime.now()
    duedate = current_time + relativedelta(days=7)

    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_duedate = duedate.strftime("%Y-%m-%d")

    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    c.execute('''
        INSERT INTO feerecord (feerecord_id, feerecord_duedate, feerecord_amount, feerecord_status, feerecord_timecreated)
        VALUES (?, ?, ?, ?, ?)
        ''', (id, formatted_duedate, amount, status, formatted_time))

    conn.commit()
    conn.close()

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

#to automatically set the fee status to overdue once it got past the due date
def create_trigger():
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    # Create the trigger
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS update_overdue_status
    AFTER UPDATE ON feerecord
    FOR EACH ROW
    BEGIN
        UPDATE feerecord
        SET feerecord_status = 'OVERDUE'
        WHERE feerecord_duedate < DATE('now') AND feerecord_status != 'OVERDUE';
    END;
    ''')

    conn.commit()
    conn.close()

#function to periodically check if a fee is overdue
def update_overdue_status():
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    # Update all overdue records
    c.execute('''
        UPDATE feerecord
        SET feerecord_status = 'OVERDUE'
        WHERE feerecord_duedate < DATE('now') AND feerecord_status != 'OVERDUE'
    ''')

    conn.commit()
    conn.close()

