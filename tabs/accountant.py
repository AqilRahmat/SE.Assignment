#TODO: Can manage fee record (add, view, update, delete)
#TODO: Generate invoice

import customtkinter as ctk
import sqlite3
import uuid
from tkinter import ttk, messagebox, filedialog
import dbfunction
import navbar
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Account(ctk.CTkFrame):
    parent_names = None

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load navigation bar
        navbar.nav(self)

        # Title label
        self.label = ctk.CTkLabel(self, text="Accountant Page", font=("Arial", 20, "bold"))
        self.label.pack(pady=15)

        # Apply styling to Treeview for better readability
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14))  # Table row font size
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))  # Table header font size
        style.configure("Treeview", rowheight=30)  # Increase row height for spacing

        # Table Frame (Displays fee records)
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Define columns for the table
        self.tree = ttk.Treeview(table_frame, columns=("FeeID", "ParentID", "DueDate", "Amount", "Status", "CreatedTime"), show="headings")
        self.tree.heading("FeeID", text="Fee Record ID")
        self.tree.heading("ParentID", text="Parent ID")
        self.tree.heading("DueDate", text="Due Date")
        self.tree.heading("Amount", text="Fee Amount (RM)")
        self.tree.heading("Status", text="Payment Status")
        self.tree.heading("CreatedTime", text="Time Created")

        # Set column widths and alignment
        self.tree.column("FeeID", width=150, anchor="center")
        self.tree.column("ParentID", width=150, anchor="center")
        self.tree.column("DueDate", width=120, anchor="center")
        self.tree.column("Amount", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("CreatedTime", width=160, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.populate_tree()  # Load table data

        # Input Frame (Form for adding/updating records)
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=20)

        # Fee Record ID input
        self.fee_id_label = ctk.CTkLabel(input_frame, text="Fee Record ID:")
        self.fee_id_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.fee_id_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Fee Record ID", width=250)
        self.fee_id_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="w")

        # choose parent name from box
        self.parent_id_label = ctk.CTkLabel(input_frame, text="Parent ID:")
        self.parent_id_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.parent_id_box = ctk.CTkComboBox(input_frame,  values=self.parent_names, width=250)
        self.parent_id_box.set("Select Parent")
        self.parent_id_box.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="w")

        self.parent_names = self.parent_box_values()

        # Fee Amount input
        self.amount_label = ctk.CTkLabel(input_frame, text="Fee Amount (RM):")
        self.amount_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.amount_entry = ctk.CTkEntry(input_frame, placeholder_text="Enter Amount", width=150)
        self.amount_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Payment Status selection
        self.status_label = ctk.CTkLabel(input_frame, text="Payment Status:")
        self.status_label.grid(row=3, column=2, padx=10, pady=5, sticky="e")
        self.status_var = ctk.StringVar(value="Pending")
        self.status_menu = ctk.CTkComboBox(input_frame, values=["Pending", "Paid"], variable=self.status_var, width=120)
        self.status_menu.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Button Frame (For managing records)
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        # Buttons for managing records
        self.add_button = ctk.CTkButton(button_frame, text="➕ Add Record", command=self.add_fee, width=160)
        self.add_button.grid(row=0, column=0, padx=10, pady=5)

        self.update_button = ctk.CTkButton(button_frame, text="✏ Update Record", command=self.update_fee, width=160)
        self.update_button.grid(row=0, column=1, padx=10, pady=5)

        self.delete_button = ctk.CTkButton(button_frame, text="🗑 Delete Record", command=self.delete_fee, width=160)
        self.delete_button.grid(row=0, column=2, padx=10, pady=5)

        self.invoice_button = ctk.CTkButton(button_frame, text="📄 Generate Invoice", command=self.generate_invoice, width=160)
        self.invoice_button.grid(row=0, column=3, padx=10, pady=5)

    def parent_box_values(self):
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute("SELECT parent_name FROM parent")
        parents = [row[0] for row in c.fetchall()]

        conn.close()
        return parents

    def populate_tree(self):
        """Loads all records into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear table
        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()
        cursor.execute("SELECT feerecord_id, parent_id, feerecord_duedate, feerecord_amount, feerecord_status, feerecord_timecreated FROM feerecord")
        for record in cursor.fetchall():
            self.tree.insert("", "end", values=record)
        conn.close()

        self.parent_names = self.parent_box_values()

    def add_fee(self):
        """Adds a new fee record."""
        fee_id = self.fee_id_entry.get().strip() or str(uuid.uuid4())  # Generate Fee ID if empty
        amount = self.amount_entry.get()
        status = self.status_var.get()
        parent = self.parent_id_box.get()

        dbfunction.insert_into_feerecorddatabase(fee_id, parent, amount, status)

        self.populate_tree()  # Refresh table
        messagebox.showinfo("Success", "Fee record added successfully!")

    def update_fee(self):
        """Updates the selected fee record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No record selected.")
            return

        item = self.tree.item(selected_item[0])
        values = item.get("values", [])

        if len(values) < 6:
            messagebox.showerror("Error", "Invalid data selected.")
            return

        record_id = values[0]  # Fee record ID
        new_amount = self.amount_entry.get()
        new_status = self.status_var.get()

        try:
            new_amount = float(new_amount)  # Ensure the amount is a valid float
            conn = sqlite3.connect("CeriaPay.db")
            cursor = conn.cursor()

            cursor.execute("UPDATE feerecord SET feerecord_amount=?, feerecord_status=? WHERE feerecord_id=?",
                           (new_amount, new_status, record_id))
            conn.commit()
            conn.close()

            self.populate_tree()  # Refresh the table to reflect changes
            messagebox.showinfo("Success", "Fee record updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def update_parent_combobox(self):
        """Updates the parent ComboBox with the latest parent names."""
        self.parent_names = self.parent_box_values()  # Fetch the updated parent names
        self.parent_id_box.configure(values=self.parent_names)

    def delete_fee(self):
        """Deletes the selected fee record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No record selected.")
            return

        item = self.tree.item(selected_item)
        record_id = item['values'][0]

        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM feerecord WHERE feerecord_id=?", (record_id,))
        conn.commit()
        conn.close()

        self.populate_tree()  # Refresh table
        messagebox.showinfo("Success", "Fee record deleted successfully!")

    def generate_invoice(self):
        """Generates an invoice as a PDF for the selected record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No record selected.")
            return

        item = self.tree.item(selected_item[0])
        values = item.get("values", [])

        if len(values) < 6:
            messagebox.showerror("Error", "Invalid data selected.")
            return

        record_id, due_date, amount, status, created_time = values

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(200, 750, "INVOICE")
            c.setFont("Helvetica", 14)
            c.drawString(100, 700, f"Invoice ID: {record_id}")
            c.drawString(100, 670, f"Due Date: {due_date}")
            c.drawString(100, 640, f"Amount: RM{amount}")
            c.drawString(100, 610, f"Status: {status}")
            c.drawString(100, 580, f"Created Time: {created_time}")
            c.save()
            messagebox.showinfo("Success", "Invoice generated successfully!")
