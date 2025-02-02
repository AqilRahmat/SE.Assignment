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

        navbar.parent_nav(self)

        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand="yes")

        #creating a frame
        self.create_frame_for_parent()

    #frame inside the window that will hold the functions
    def create_frame_for_parent(self):
        self.fees_frame()
        self.history_frame()
        self.populate_parent_tree()

    def fees_frame(self):
        # Create fees frame with padding and background color
        fees_frame = ctk.CTkFrame(self.scrollable_frame,
                                  fg_color="#f0f0f0",
                                  border_width=2,
                                  border_color="#d1d1d1",
                                  corner_radius=10)
        fees_frame.pack(fill='x', pady=10, padx=15, expand=True)

        # Amount frame (left side) with padding
        amount_frame = ctk.CTkFrame(fees_frame,
                                    fg_color="#ffffff",
                                    corner_radius=10)
        amount_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)  # Add padding around frame

        amount_label = ctk.CTkLabel(amount_frame,
                                    text="AMOUNT",
                                    font=("Arial", 14, "bold"),
                                    text_color="black")
        amount_label.pack(fill='x', pady=5)  # Make label fill horizontally

        amount_owed = self.get_amount_owed()

        amount_number = ctk.CTkLabel(amount_frame,
                                     text=amount_owed,
                                     font=("Arial", 12),
                                     text_color="black")
        amount_number.pack(fill='x', pady=5)  # Make label fill horizontally

        # Due date frame (right side) with padding
        duedate_frame = ctk.CTkFrame(fees_frame,
                                     fg_color="#ffffff",
                                     corner_radius=10)
        duedate_frame.pack(side='left', fill='both', expand=True, padx=10, pady=5)  # Add padding around frame

        duedate_label = ctk.CTkLabel(duedate_frame,
                                     text="DATE DUE",
                                     font=("Arial", 14, "bold"),
                                     text_color="black")
        duedate_label.pack(fill='x', pady=5)  # Make label fill horizontally

        duedate_actual = self.get_due_date()

        duedate_time = ctk.CTkLabel(duedate_frame,
                                    text=duedate_actual,
                                    font=("Arial", 12),
                                    text_color="black")
        duedate_time.pack(fill='x', pady=5)  # Make label fill horizontally

        # Payment button placed at the bottom of the fees_frame, aligned right
        payment_button = ctk.CTkButton(fees_frame, text="Make Payment", command=self.payment_window)
        payment_button.pack(side="left", fill='both', padx=10, pady=10)

    def get_due_date(self):
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        amount  = c.execute("SELECT feerecord_duedate FROM feerecord WHERE feerecord_status = 'OVERDUE' or feerecord_status = 'Pending' ORDER BY feerecord_duedate ASC LIMIT 1")

        amount = amount.fetchone()[0]

        c.close()

        return amount

    def get_amount_owed(self):
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        amount  = c.execute("SELECT feerecord_amount FROM feerecord WHERE feerecord_status = 'OVERDUE' or feerecord_status = 'Pending' ORDER BY feerecord_duedate ASC LIMIT 1")

        amount = amount.fetchone()[0]

        c.close()

        return amount


    def history_frame(self):
        table_frame = ctk.CTkFrame(self.scrollable_frame,
                                   fg_color="#f0f0f0",
                                   border_width=2,
                                   border_color="#d1d1d1",
                                   corner_radius=15)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(table_frame, columns=("id", "date", "amount", "status"), show="headings")

        # Define column headings
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Due Date")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("status", text="Status")

        # Define column widths
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("amount", width=100, anchor="center")
        self.tree.column("status", width=150, anchor="center")

        # Add a vertical scrollbar for the table
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill="both", expand=True)

    #payment window
    def payment_window(self):
        payment = ctk.CTkToplevel()
        payment.attributes("-topmost", True)

        payment.title("Payment")
        payment.geometry("500x500")

        label = ctk.CTkLabel(payment, text="Payment")
        label.pack()

    # popup for profile window
    def profile_window(self):
        profile = ctk.CTkToplevel()
        profile.attributes("-topmost", True)

        profile.title("User Profile")
        profile.geometry("500x500")

        label = ctk.CTkLabel(profile, text="User Profile")
        label.pack()

        # Username Label
        username = Login.username_for_profile
        username_label = ctk.CTkLabel(profile, text=username)
        username_label.pack()

        # contact num change
        number_label = ctk.CTkLabel(profile, text="Phone Number")
        number_label.pack(pady=5, padx=5)

        phonenum = Login.phonenum_for_profile
        self.real_number_label = ctk.CTkLabel(profile, text=phonenum)
        self.real_number_label.pack(pady=5, padx=5)

        self.number_change_field = ctk.CTkEntry(profile, placeholder_text="Insert new Number")
        self.number_change_field.pack(pady=5)

        self.number_change_button = ctk.CTkButton(profile, text="Change Number", command=self.number_change)
        self.number_change_button.pack(pady=5)

        #Password label & textfield to change
        password_label = ctk.CTkLabel(profile, text="Password")
        password_label.pack(pady=5, padx=5)

        self.password_change_field = ctk.CTkEntry(profile, show="*", placeholder_text="Insert New Password")
        self.password_change_field.pack(pady=5)

        self.password_change_button = ctk.CTkButton(profile, text="Change Password", command=self.password_change)
        self.password_change_button.pack(pady=5)

    def password_change(self):
        new_password = self.password_change_field.get()
        if new_password == Login.password_for_profile:
            messagebox.showinfo("ERROR", "New password cannot be the same as the old one.")
            self.password_change_field.delete(0, 'end')
            return
        else:
            dbfunction.update_entry('parent', 'parent_password', new_password, 'parent_id', Login.ic_for_profile)
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
        print(parent_id_for_tree)
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
