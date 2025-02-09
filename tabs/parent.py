#TODO: Can view fees, and make payment, can also view payment history
#   GUI Done, just need to add functionality
import sqlite3
from tkinter import ttk, messagebox, PhotoImage
import customtkinter as ctk

import dbfunction
import navbar
from tabs.login import Login


class Parent(ctk.CTkFrame):
    phonenum = None

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ctk.set_appearance_mode("light")  # Light mode for pastel colors

        navbar.parent_nav(self)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="#F8F9FA")  # Soft gray background
        self.scrollable_frame.pack(fill="both", expand="yes")

        self.label = ctk.CTkLabel(self.scrollable_frame, text="Parent Page", font=("Arial", 20, "bold"), text_color="#4A4E69")
        self.label.pack(pady=15)

        self.fees_frame()
        self.history_frame()
        self.create_frame_for_parent()

    # Frame inside the window that will hold the functions
    def create_frame_for_parent(self):
        self.populate_parent_tree()
        self.update_all_labels()

    def fees_frame(self):
        self.get_payment_frame_values()

        fees_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#EDE7F6", corner_radius=15, border_width=1, border_color="#BDBDBD")  # Light Lavender
        fees_frame.pack(fill='x', pady=15, padx=20, expand=True)

        amount_frame = ctk.CTkFrame(fees_frame, fg_color="#EDE7F6", corner_radius=15)  # Light Pink
        amount_frame.pack(side='left', fill='both', expand=True, padx=15, pady=10)

        amount_label = ctk.CTkLabel(amount_frame, text="AMOUNT", font=("Arial", 16, "bold"), text_color="#4A4E69")  # Muted Navy
        amount_label.pack(pady=5)

        self.amount_number = ctk.CTkLabel(amount_frame, text=self.amount_owed, font=("Arial", 14), text_color="#4A4E69")
        self.amount_number.pack()

        duedate_frame = ctk.CTkFrame(fees_frame, fg_color="#EDE7F6", corner_radius=15)
        duedate_frame.pack(side='left', fill='both', expand=True, padx=15, pady=10)

        duedate_label = ctk.CTkLabel(duedate_frame, text="DATE DUE", font=("Arial", 16, "bold"), text_color="#4A4E69")
        duedate_label.pack(pady=5)

        self.duedate_time = ctk.CTkLabel(duedate_frame, text=self.duedate_actual, font=("Arial", 14), text_color="#4A4E69")
        self.duedate_time.pack()

        payment_button = ctk.CTkButton(fees_frame, text="Make Payment", font=("Arial", 14, "bold"), corner_radius=10,
                                       fg_color="#A2D2FF", hover_color="#BDE0FE", text_color="black",
                                       command=self.payment_window)
        payment_button.pack(side="left", fill='both', padx=15, pady=10)

    def get_payment_frame_values(self):
        """Fetch the next due date and amount owed."""
        self.duedate_actual = self.get_due_date()
        self.amount_owed = self.get_amount_owed()

    def get_due_date(self):
        """Fetch the earliest due date for pending or overdue payments."""
        id = Login.ic_for_profile
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute(
            """SELECT feerecord_duedate 
               FROM feerecord 
               WHERE (feerecord_status = 'OVERDUE' OR feerecord_status = 'Pending') 
               AND parent_id = ? 
               ORDER BY feerecord_timecreated ASC 
               LIMIT 1""",
            (id,)
        )

        result = c.fetchone()
        c.close()
        conn.close()

        return result[0] if result else "No Outstanding Invoice"

    def get_amount_owed(self):
        """Fetch the amount owed for the earliest pending or overdue payment."""
        id = Login.ic_for_profile
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute(
            """SELECT feerecord_amount 
               FROM feerecord 
               WHERE (feerecord_status = 'OVERDUE' OR feerecord_status = 'Pending') 
               AND parent_id = ? 
               ORDER BY feerecord_timecreated ASC 
               LIMIT 1""",
            (id,)
        )

        result = c.fetchone()
        c.close()
        conn.close()

        return result[0] if result else "0"

    def history_frame(self):
        """Create a frame for the payment history table."""
        table_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="#EDE7F6", border_width=1, border_color="#BDBDBD", corner_radius=15)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        label = ctk.CTkLabel(table_frame, text="Payment History", font=("Arial", 18, "bold"), text_color="#4A4E69")
        label.pack(pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("id", "date", "amount", "status"), show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Due Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("amount", width=100, anchor="center")
        self.tree.column("status", width=150, anchor="center")

        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill="both", expand=True)

    def update_all_labels(self):
        """Refresh all labels and the payment history table."""
        self.get_payment_frame_values()

        # Update the labels showing due date and amount owed
        self.amount_number.configure(text=self.amount_owed)  # Update the amount owed label
        self.duedate_time.configure(text=self.duedate_actual)  # Update the due date label

        # Refresh the table/treeview for payment history
        self.populate_parent_tree()

    def payment_window(self):
        """Create a payment window for the parent to make payments."""
        payment = ctk.CTkToplevel()
        payment.attributes("-topmost", True)

        payment.title("Payment")
        payment.geometry("400x400")

        ctk.CTkLabel(payment, text="Make a Payment", font=("Arial", 18, "bold"), text_color="#4A4E69").pack(pady=15)

        id_label = ctk.CTkLabel(payment, text="Record ID:", font=("Arial", 14))
        id_label.pack(pady=5)
        self.id_entry = ctk.CTkEntry(payment)
        self.id_entry.pack(pady=5)

        amount_label = ctk.CTkLabel(payment, text="Amount:", font=("Arial", 14))
        amount_label.pack(pady=5)
        self.amount_entry = ctk.CTkEntry(payment)
        self.amount_entry.pack(pady=5)

        self.payment_method = ctk.StringVar()
        self.payment_method.set("Credit Card")

        ctk.CTkLabel(payment, text="Payment Method:", font=("Arial", 14)).pack(pady=5)

        options_frame = ctk.CTkFrame(payment, fg_color="transparent")
        options_frame.pack()

        ctk.CTkRadioButton(options_frame, text="Credit Card", variable=self.payment_method, value="Credit Card").pack(side="left", padx=40)
        ctk.CTkRadioButton(options_frame, text="Debit Card", variable=self.payment_method, value="Debit Card").pack(side="left", padx=10)
        ctk.CTkRadioButton(options_frame, text="FPX", variable=self.payment_method, value="FPX").pack(side="left", padx=10)

        submit_button = ctk.CTkButton(payment, text="Submit Payment", fg_color="#FFAFCC", hover_color="#FDCFE8",
                                      text_color="black", command=self.process_payment)
        submit_button.pack(pady=20)

    def process_payment(self):
        """Process the payment and update the database."""
        record_id = self.id_entry.get()
        amount = self.amount_entry.get()

        # Fetch the amount owed from the database
        amount_owed = dbfunction.fetch_entry('feerecord_amount', 'feerecord', 'feerecord_id', record_id)

        # Validate the entries
        if not record_id or not amount:
            messagebox.showerror("Error", "Please fill in both the Record ID and Amount.")
            return

        try:
            amount = float(amount)  # Convert user input to float
            amount_owed = float(amount_owed) if amount_owed else 0  # Convert DB value to float

            # Ensure entered amount is at least the amount owed
            if amount < amount_owed:
                messagebox.showerror("Error", "Amount must be equal to or greater than the amount owed.")
                return

        except ValueError:
            messagebox.showerror("Error", "Amount must be a valid number.")
            return

        # If validation passes, update the database and labels
        self.update_feerecord(record_id)
        self.update_all_labels()

        messagebox.showinfo("Success", "Payment processed successfully!")

    def update_feerecord(self, record_id):
        """Mark the fee record as 'Paid' in the database."""
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute("UPDATE feerecord SET feerecord_status = 'Paid' WHERE feerecord_id = ? AND parent_id = ?",
                  (record_id, Login.ic_for_profile))

        conn.commit()
        c.close()
        conn.close()

    def populate_parent_tree(self):
        """Loads all records into the payment history table."""
        parent_id_for_tree = Login.ic_for_profile
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear table
        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT feerecord_id, feerecord_duedate, feerecord_amount, feerecord_status FROM feerecord WHERE parent_id = ? ORDER BY feerecord_duedate ASC",
            (parent_id_for_tree,))
        for record in cursor.fetchall():
            self.tree.insert("", "end", values=record)
        conn.close()
