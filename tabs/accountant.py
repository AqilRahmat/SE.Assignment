#TODO: Can manage fee record (add, view, update, delete)
#TODO: Generate invoice

import customtkinter as ctk
import sqlite3
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

        # ---------------------- TABLE ----------------------------------------------------------------
        table_frame = ctk.CTkFrame(self)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame,
                                 columns=("FeeID", "ParentID", "DueDate", "Amount", "Status", "CreatedTime"),
                                 show="headings")
        self.tree.heading("FeeID", text="Fee Record ID")
        self.tree.heading("ParentID", text="Parent ID")
        self.tree.heading("DueDate", text="Due Date")
        self.tree.heading("Amount", text="Fee Amount (RM)")
        self.tree.heading("Status", text="Payment Status")
        self.tree.heading("CreatedTime", text="Time Created")

        self.tree.column("FeeID", width=150, anchor="center")
        self.tree.column("ParentID", width=150, anchor="center")
        self.tree.column("DueDate", width=120, anchor="center")
        self.tree.column("Amount", width=100, anchor="center")
        self.tree.column("Status", width=100, anchor="center")
        self.tree.column("CreatedTime", width=160, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<ButtonRelease-1>", self.select_record)  # Event binding for selecting a record

        # ---------------------- TABVIEW -------------------------------------------------------------------------------
        tab_frame = ctk.CTkFrame(self)
        tab_frame.pack(pady=10, padx=20, fill="both", expand=False)

        self.tabview = ctk.CTkTabview(tab_frame, width=500, height=220)  # Reduced size
        self.tabview.pack(expand=False, padx=10, pady=5, fill="both")  # Adjusted padding for compact layout

        self.manage_tab = self.tabview.add("📋 Manage Fee Record")
        self.update_tab = self.tabview.add("✏ Update Fee Record")
        self.invoice_tab = self.tabview.add("📄 Generate Invoice")

        self.parent_names = self.parent_box_values()

        # ---------------------- MANAGE FEE RECORD TAB -------------------------------------------------------------------
        manage_grid = ctk.CTkFrame(self.manage_tab)
        manage_grid.pack(pady=5, padx=10, fill="both", expand=True)

        self.fee_id_label = ctk.CTkLabel(manage_grid, text="Fee ID:")
        self.fee_id_label.grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.fee_id_entry = ctk.CTkEntry(manage_grid, width=200)
        self.fee_id_entry.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        self.parent_id_label = ctk.CTkLabel(manage_grid, text="Parent:")
        self.parent_id_label.grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self.parent_id_box = ctk.CTkComboBox(manage_grid, values=self.parent_names, width=200)
        self.parent_id_box.set("Select Parent")
        self.parent_id_box.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        self.amount_label = ctk.CTkLabel(manage_grid, text="Amount (RM):")
        self.amount_label.grid(row=2, column=0, padx=5, pady=3, sticky="e")
        self.amount_entry = ctk.CTkEntry(manage_grid, width=150)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=3, sticky="w")

        self.status_label = ctk.CTkLabel(manage_grid, text="Status:")
        self.status_label.grid(row=3, column=0, padx=5, pady=3, sticky="e")
        self.status_var = ctk.StringVar(value="Pending")
        self.status_menu = ctk.CTkComboBox(manage_grid, values=["Pending", "Paid"], variable=self.status_var, width=150)
        self.status_menu.grid(row=3, column=1, padx=5, pady=3, sticky="w")

        # New Frame for Buttons
        button_frame = ctk.CTkFrame(manage_grid)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

        self.add_button = ctk.CTkButton(button_frame, text="➕ Add Fee", command=self.add_fee, width=140)
        self.add_button.pack(side="left", padx=10, pady=5, expand=True)

        self.delete_button = ctk.CTkButton(button_frame, text="🗑 Delete Fee", command=self.delete_fee, width=140)
        self.delete_button.pack(side="right", padx=10, pady=5, expand=True)

        # ---------------------- UPDATE FEE RECORD TAB --------------------------------------------------------------------------
        update_grid = ctk.CTkFrame(self.update_tab)
        update_grid.pack(pady=5, padx=10, fill="both", expand=True)

        self.update_amount_label = ctk.CTkLabel(update_grid, text="New Amount:")
        self.update_amount_label.grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.update_amount_entry = ctk.CTkEntry(update_grid, width=150)
        self.update_amount_entry.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        self.update_status_label = ctk.CTkLabel(update_grid, text="New Status:")
        self.update_status_label.grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self.update_status_var = ctk.StringVar(value="Pending")
        self.update_status_menu = ctk.CTkComboBox(update_grid, values=["Pending", "Paid"],
                                                  variable=self.update_status_var, width=150)
        self.update_status_menu.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        self.update_button = ctk.CTkButton(update_grid, text="✏ Update", command=self.update_fee, width=100)
        self.update_button.grid(row=2, column=1, padx=5, pady=5)

        # ---------------------- GENERATE INVOICE TAB ------------------------------------------------------------------------------
        invoice_grid = ctk.CTkFrame(self.invoice_tab)
        invoice_grid.pack(pady=5, padx=10, fill="both", expand=True)

        self.invoice_label = ctk.CTkLabel(invoice_grid, text="Select a record and generate an invoice",
                                          font=("Arial", 12))
        self.invoice_label.pack(pady=5)

        self.generate_invoice_button = ctk.CTkButton(invoice_grid, text="📄 Generate Invoice",
                                                     command=self.generate_invoice, width=180)
        self.generate_invoice_button.pack(pady=5)

        self.populate_tree()  # Load table data

    def parent_box_values(self):
        """Fetch parent names from the database."""
        conn = sqlite3.connect("CeriaPay.db")
        c = conn.cursor()

        c.execute("SELECT parent_name FROM parent")
        parents = [row[0] for row in c.fetchall()]

        conn.close()
        return parents

    def populate_tree(self):
        """Loads all fee records into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT feerecord.feerecord_id, parent.parent_name, feerecord.feerecord_duedate, 
                   feerecord.feerecord_amount, feerecord.feerecord_status, feerecord.feerecord_timecreated
            FROM feerecord
            JOIN parent ON feerecord.parent_id = parent.parent_id
        """)

        records = cursor.fetchall()

        for record in records:
            self.tree.insert("", "end", values=record)

        conn.close()

    def add_fee(self):
        """Adds a new fee record, ensuring no duplicate Fee Record ID."""
        fee_id = self.fee_id_entry.get().strip()
        amount = self.amount_entry.get().strip()
        status = self.status_var.get()
        parent = self.parent_id_box.get().strip()

        # Validation checks
        if not fee_id:
            messagebox.showerror("Error", "Fee Record ID cannot be empty.")
            return

        if not amount:
            messagebox.showerror("Error", "Fee Amount cannot be empty.")
            return

        try:
            amount = float(amount)  # Ensure it's a valid number
            if amount <= 0:
                messagebox.showerror("Error", "Fee Amount must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Fee Amount must be a valid number.")
            return

        if parent == "Select Parent":
            messagebox.showerror("Error", "Please select a Parent.")
            return

        # Check for duplicate Fee Record ID
        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM feerecord WHERE feerecord_id = ?", (fee_id,))
        result = cursor.fetchone()[0]

        if result > 0:
            messagebox.showerror("Error", "Cannot enter duplicate Fee Record ID. Please use a unique ID.")
            conn.close()
            return

        # Insert into database using dbfunction module
        try:
            dbfunction.insert_into_feerecorddatabase(fee_id, parent, amount, status)
            self.populate_tree()  # Refresh table
            messagebox.showinfo("Success", "Fee record added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Database error: Could not insert record.")
        finally:
            conn.close()

    def update_fee(self):
        """Updates the fee amount and status based on the selected record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a fee record from the table before updating.")
            return

        item = self.tree.item(selected_item[0])
        fee_id = item["values"][0]  # Fee Record ID
        new_amount = self.update_amount_entry.get().strip()
        new_status = self.update_status_var.get()

        if not new_amount:
            messagebox.showerror("Error", "Fee Amount cannot be empty.")
            return

        try:
            new_amount = float(new_amount)
            conn = sqlite3.connect("CeriaPay.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE feerecord SET feerecord_amount=?, feerecord_status=? WHERE feerecord_id=?",
                           (new_amount, new_status, fee_id))
            conn.commit()
            conn.close()
            self.populate_tree()
            messagebox.showinfo("Success", "Fee record updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def update_parent_combobox(self):
        """Updates the parent ComboBox with the latest parent names."""
        self.parent_names = self.parent_box_values()  # Fetch the updated parent names
        self.parent_id_box.configure(values=self.parent_names)

    def delete_fee(self):
        """Deletes the selected fee record from the table."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a fee record from the table before deleting.")
            return

        item = self.tree.item(selected_item[0])
        record_id = item["values"][0]  # Fee Record ID

        confirmation = messagebox.askyesno("Confirm Deletion",
                                           f"Are you sure you want to delete Fee Record ID {record_id}?")
        if not confirmation:
            return

        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM feerecord WHERE feerecord_id=?", (record_id,))
        conn.commit()
        conn.close()

        self.populate_tree()  # Refresh table
        messagebox.showinfo("Success", "Fee record deleted successfully!")

    def select_record(self, event):
        """Fetches selected record and pre-fills update fields, but does not switch to the update tab automatically."""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        values = item.get("values", [])

        if values:
            self.update_amount_entry.delete(0, 'end')
            self.update_amount_entry.insert(0, str(values[3]))  # Fee Amount
            self.update_status_var.set(values[4])  # Status

    def generate_invoice(self):
        """Generates an invoice as a PDF for the selected record."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a fee record from the table before generating an invoice.")
            return

        item = self.tree.item(selected_item[0])
        values = item.get("values", [])

        if not values:
            messagebox.showerror("Error", "No fee record found.")
            return

        fee_id = values[0]  # Fee Record ID
        parent_name = values[1]  # Parent Name
        due_date = values[2]  # Due Date
        amount = values[3]  # Fee Amount
        status = values[4]  # Payment Status
        created_time = values[5]  # Time Created

        # Ask user where to save the PDF file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save Invoice As",
            initialfile=f"Invoice_{fee_id}.pdf"
        )

        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(200, 750, "INVOICE")
            c.setFont("Helvetica", 14)

            # Draw invoice details
            c.drawString(100, 700, f"Invoice ID: {fee_id}")
            c.drawString(100, 670, f"Parent Name: {parent_name}")
            c.drawString(100, 640, f"Due Date: {due_date}")
            c.drawString(100, 610, f"Amount: RM{amount}")
            c.drawString(100, 580, f"Status: {status}")
            c.drawString(100, 550, f"Created Time: {created_time}")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(100, 500, "Thank you for your payment!")

            c.save()
            messagebox.showinfo("Success", f"Invoice generated successfully!")
