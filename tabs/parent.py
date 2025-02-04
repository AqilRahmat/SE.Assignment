#TODO: Can view fees, and make payment, can also view payment history
#   GUI Done, just need to add functionality
import sqlite3
from tkinter import ttk, messagebox
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

        self.fees_frame()
        self.history_frame()
        self.create_frame_for_parent()

    #frame inside the window that will hold the functions
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
        self.duedate_actual = self.get_due_date()
        self.amount_owed = self.get_amount_owed()

    def get_due_date(self):
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute(
            "SELECT feerecord_duedate "
            "FROM feerecord "
            "WHERE feerecord_status = 'OVERDUE' OR feerecord_status = 'Pending' "
            "ORDER BY feerecord_timecreated ASC "
            "LIMIT 1")

        result = c.fetchone()

        c.close()

        return result[0] if result else "No Outstanding Invoice"

    def get_amount_owed(self):
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute(
            "SELECT feerecord_amount "
            "FROM feerecord "
            "WHERE feerecord_status = 'OVERDUE' OR feerecord_status = 'Pending' "
            "ORDER BY feerecord_timecreated ASC LIMIT 1")

        result = c.fetchone()

        c.close()

        return result[0] if result else "0"


    def history_frame(self):
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
        # Fetch updated due date and amount owed from the database
        self.get_payment_frame_values()

        # Update the labels showing due date and amount owed
        self.amount_number.configure(text=self.amount_owed)  # Update the amount owed label
        self.duedate_time.configure(text=self.duedate_actual)  # Update the due date label

        # Refresh the table/treeview for payment history to reflect the current data
        self.populate_parent_tree()

    #payment window
    def payment_window(self):
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

        ctk.CTkRadioButton(options_frame, text="Credit Card", variable=self.payment_method, value="Credit Card").pack(side="left", padx=10)
        ctk.CTkRadioButton(options_frame, text="Debit Card", variable=self.payment_method, value="Debit Card").pack(side="left", padx=10)
        ctk.CTkRadioButton(options_frame, text="FPX", variable=self.payment_method, value="FPX").pack(side="left", padx=10)

        submit_button = ctk.CTkButton(payment, text="Submit Payment", fg_color="#FFAFCC", hover_color="#FDCFE8",
                                      text_color="black", command=self.process_payment)
        submit_button.pack(pady=20)


    def process_payment(self):
        record_id = self.id_entry.get()
        amount = self.amount_entry.get()

        # Validate the entries
        if not record_id or not amount:
            messagebox.showerror("Error", "Please fill in both the Record ID and Amount.")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        #if pass validation
        self.update_feerecord()
        self.update_all_labels()

    def update_feerecord(self):
        record_id = self.id_entry.get()
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute("UPDATE feerecord SET feerecord_status = 'Paid' WHERE feerecord_id = ? AND parent_id = ? ", (record_id, Login.username_for_profile))

        conn.commit()
        c.close()
        self.get_payment_frame_values()
        self.populate_parent_tree()

    # popup for profile window
    def profile_window(self):
        profile = ctk.CTkToplevel()
        profile.attributes("-topmost", True)

        profile.title("User Profile")
        profile.geometry("400x400")

        ctk.CTkLabel(profile, text="User Profile", font=("Arial", 18, "bold"), text_color="#4A4E69").pack(pady=15)

        username_label = ctk.CTkLabel(profile, text=f"Username: {Login.username_for_profile}", font=("Arial", 14))
        username_label.pack(pady=5)

        number_label = ctk.CTkLabel(profile, text="Phone Number:", font=("Arial", 14))
        number_label.pack(pady=5)

        self.real_number_label = ctk.CTkLabel(profile, text=Login.phonenum_for_profile, font=("Arial", 14, "bold"))
        self.real_number_label.pack(pady=5)

        self.number_change_field = ctk.CTkEntry(profile, placeholder_text="Insert new Number")
        self.number_change_field.pack(pady=5)

        ctk.CTkButton(profile, text="Change Number", command=self.number_change, fg_color="#FFAFCC", hover_color="#FDCFE8", text_color='black').pack(pady=5)

        password_label = ctk.CTkLabel(profile, text="Password:", font=("Arial", 14))
        password_label.pack(pady=5)

        self.password_change_field = ctk.CTkEntry(profile, show="*", placeholder_text="Insert New Password")
        self.password_change_field.pack(pady=5)

        ctk.CTkButton(profile, text="Change Password", command=self.password_change, fg_color="#A2D2FF", hover_color="#BDE0FE", text_color='black').pack(pady=5)

    def password_change(self):
        new_password = self.password_change_field.get()
        if new_password == Login.password_for_profile:
            messagebox.showinfo("ERROR", "New password cannot be the same as the old one.")
            self.password_change_field.delete(0, 'end')
            return
        else:
            dbfunction.update_entry('parent', 'parent_password', new_password, 'parent_id', Login.ic_for_profile)

            Login.password_for_profile = new_password
            messagebox.showinfo("Password changed", "Password changed successfully!")
            self.password_change_field.delete(0, 'end')
            return

    def number_change(self):
        new_number = self.number_change_field.get()
        if new_number == Login.phonenum_for_profile:
            messagebox.showinfo("ERROR", "New number cannot be the same as the old one.")
            self.number_change_field.delete(0, 'end')
            return
        else:
            # Update the phone number in the database
            dbfunction.update_entry('parent', 'parent_contactnum', new_number, 'parent_id', Login.ic_for_profile)

            # Update the phonenum in the Login class and real_number_label
            Login.phonenum_for_profile = new_number
            self.real_number_label.configure(text=Login.phonenum_for_profile)

            # Explicitly refresh the label
            self.real_number_label.update_idletasks()  # Force UI to update

            # Show success message
            messagebox.showinfo("Number changed", "Number changed successfully!")

            # Clear the input field
            self.number_change_field.delete(0, 'end')
            return

    def populate_parent_tree(self):
        parent_id_for_tree = Login.ic_for_profile
        """Loads all records into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear table
        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT feerecord_id , feerecord_duedate, feerecord_amount, feerecord_status FROM feerecord WHERE parent_id = ? ORDER BY feerecord_duedate ASC", (parent_id_for_tree,))
        for record in cursor.fetchall():
            self.tree.insert("", "end", values=record)
        conn.close()
