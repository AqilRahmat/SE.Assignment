#use this file to make the functions to change anything inside the database
import sqlite3

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

#fetch data from the table
def fetch_entry(column, table, condition_column, condition_value):
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    query = "SELECT {} FROM {} WHERE {} = ?".format(column, table, condition_column)
    c.execute(query, (condition_value,))

    result = c.fetchone()

    conn.close()

    return result[0] if result else None

#Insert into parent table
def insert_into_parentdatabase(parentid, name, contact, user, password):
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    c.execute('''
    INSERT INTO parent (parent_id, parent_name, parent_contactnum, parent_username, parent_password)
    VALUES(?,?,?,?,?)
    ''', (parentid, name, contact, user, password))

    conn.commit()
    conn.close()

#insert into admin (this is for admin only)
def insert_into_admindatabase(admin_id, admin_name, admin_contactnum, admin_username, admin_password):
    conn = sqlite3.connect("CeriaPay.db")
    try:
        c = conn.cursor()
        c.execute("""
            INSERT INTO administrator (admin_id, admin_name, admin_contactnum, admin_username, admin_password)
            VALUES (?, ?, ?, ?, ?)
        """, (admin_id, admin_name, admin_contactnum, admin_username, admin_password))
        conn.commit()
    finally:
        conn.close()  # Always close the connection

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
def insert_into_feerecorddatabase(id, parent_id, amount, status):
    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    current_time = datetime.now()
    duedate = current_time + relativedelta(days=7)

    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_duedate = duedate.strftime("%Y-%m-%d")

    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    c.execute('''
        INSERT INTO feerecord (feerecord_id, parent_id, feerecord_duedate, feerecord_amount, feerecord_status, feerecord_timecreated)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (id, parent_id, formatted_duedate, amount, status, formatted_time))

    conn.commit()
    conn.close()

#to automatically set the fee status to overdue once it got past the due date
def create_trigger():
    conn = sqlite3.connect("CeriaPay.db")
    c = conn.cursor()

    # Create the trigger with the condition to avoid changing paid records
    c.execute('''
    CREATE TRIGGER IF NOT EXISTS update_overdue_status
    AFTER UPDATE ON feerecord
    FOR EACH ROW
    BEGIN
        UPDATE feerecord
        SET feerecord_status = 'OVERDUE'
        WHERE feerecord_duedate < DATE('now') 
        AND feerecord_status != 'OVERDUE'
        AND feerecord_status != 'Paid';  
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
        WHERE feerecord_duedate < DATE('now') 
        AND feerecord_status != 'OVERDUE'
        AND feerecord_status != 'Paid';
    ''')

    # Commit and close connection
    conn.commit()

    conn.close()