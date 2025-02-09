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
        ctk.set_appearance_mode("light")  # Light mode for pastel theme
        self.configure(fg_color="#F8F9FA")  # Seamless soft gray background

        navbar.nav(self)

        self.label = ctk.CTkLabel(self, text="Accountant Page", font=("Arial", 20, "bold"), text_color="#4A4E69")
        self.label.pack(pady=15)

        # ---------------------- TABLE ----------------------------------------------------------------
        table_frame = ctk.CTkFrame(self, fg_color="#EDE7F6", border_width=1, border_color="#BDBDBD", corner_radius=15)
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

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(table_frame, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_record)

        # ---------------------- TABVIEW -------------------------------------------------------------------------------
        tab_frame = ctk.CTkFrame(self, fg_color="#F8F9FA")  # Blends perfectly
        tab_frame.pack(pady=10, padx=20, expand=False)

        self.tabview = ctk.CTkTabview(tab_frame, text_color='black', fg_color="#F8F9FA",
                                      segmented_button_selected_color="#A2D2FF",
                                      segmented_button_selected_hover_color="#BDE0FE",
                                      segmented_button_fg_color='#FFAFCC',
                                      segmented_button_unselected_color="#FFAFCC",
                                      segmented_button_unselected_hover_color="#FF8AB3")
        self.tabview.pack(expand=False, padx=10, pady=5, fill="both")

        self.manage_tab = self.tabview.add("📋 Manage Fee Record")
        self.update_tab = self.tabview.add("✏ Update Fee Record")
        self.invoice_tab = self.tabview.add("📄 Generate Invoice")

        self.parent_names = self.parent_box_values()

        # ---------------------- MANAGE FEE RECORD TAB -------------------------------------------------------------------
        manage_grid = ctk.CTkFrame(self.manage_tab, fg_color="#EDE7F6", corner_radius=15)
        manage_grid.pack(pady=5, padx=10, fill="both", expand=True)

        self.fee_id_label = ctk.CTkLabel(manage_grid, text="Fee ID:", text_color="#4A4E69")
        self.fee_id_label.grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.fee_id_entry = ctk.CTkEntry(manage_grid, width=200, border_color='white')
        self.fee_id_entry.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        self.parent_id_label = ctk.CTkLabel(manage_grid, text="Parent:", text_color="#4A4E69")
        self.parent_id_label.grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self.parent_id_box = ctk.CTkComboBox(manage_grid, values=self.parent_names, width=200, border_color='white')
        self.parent_id_box.set("Select Parent")
        self.parent_id_box.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        self.amount_label = ctk.CTkLabel(manage_grid, text="Amount (RM):", text_color="#4A4E69")
        self.amount_label.grid(row=2, column=0, padx=5, pady=3, sticky="e")
        self.amount_entry = ctk.CTkEntry(manage_grid, width=150, border_color='white')
        self.amount_entry.grid(row=2, column=1, padx=5, pady=3, sticky="w")

        self.status_label = ctk.CTkLabel(manage_grid, text="Status:", text_color="#4A4E69")
        self.status_label.grid(row=3, column=0, padx=5, pady=3, sticky="e")
        self.status_var = ctk.StringVar(value="Pending")
        self.status_menu = ctk.CTkComboBox(manage_grid, values=["Pending", "Paid"], variable=self.status_var, width=150, border_color='white')
        self.status_menu.grid(row=3, column=1, padx=5, pady=3, sticky="w")

        # New Frame for Buttons
        # Button Frame (Centered)
        button_frame = ctk.CTkFrame(manage_grid, fg_color="transparent")
        button_frame.grid(row=4, column=0, columnspan=2, pady=10, padx=5, sticky="nsew")

        # Expand frame to allow centering
        manage_grid.columnconfigure(0, weight=1)
        manage_grid.columnconfigure(1, weight=1)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Add Fee Button (Centered)
        self.add_button = ctk.CTkButton(button_frame, text="➕ Add Fee", fg_color="#A2D2FF", hover_color="#BDE0FE",
                                        text_color="#4A4E69", command=self.add_fee)
        self.add_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Delete Fee Button (Centered)
        self.delete_button = ctk.CTkButton(button_frame, text="🗑 Delete Fee", fg_color="#FFAFCC", hover_color="#FF8AB3",
                                           text_color="#4A4E69", command=self.delete_fee)
        self.delete_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # ---------------------- UPDATE FEE RECORD TAB --------------------------------------------------------------------------
        update_grid = ctk.CTkFrame(self.update_tab, fg_color="#EDE7F6", corner_radius=15)
        update_grid.pack(pady=5, padx=10, fill="both", expand=True)

        self.update_amount_label = ctk.CTkLabel(update_grid, text="New Amount:", text_color="#4A4E69")
        self.update_amount_label.grid(row=0, column=0, padx=5, pady=3, sticky="e")
        self.update_amount_entry = ctk.CTkEntry(update_grid, width=150, border_color='white')
        self.update_amount_entry.grid(row=0, column=1, padx=5, pady=3, sticky="w")

        self.update_status_label = ctk.CTkLabel(update_grid, text="New Status:", text_color="#4A4E69")
        self.update_status_label.grid(row=1, column=0, padx=5, pady=3, sticky="e")
        self.update_status_var = ctk.StringVar(value="Pending")
        self.update_status_menu = ctk.CTkComboBox(update_grid, values=['Pending', 'Paid'],
                                                  variable=self.update_status_var, width=150, border_color='white')
        self.update_status_menu.grid(row=1, column=1, padx=5, pady=3, sticky="w")

        # Button Frame for Update Button
        update_button_frame = ctk.CTkFrame(update_grid, fg_color="transparent")
        update_button_frame.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="nsew")

        # Expand the grid to make sure the button is centered
        update_grid.columnconfigure(0, weight=1)
        update_grid.columnconfigure(1, weight=1)
        update_button_frame.columnconfigure(0, weight=1)

        # Update Fee Button (Centered)
        self.update_button = ctk.CTkButton(update_button_frame, text="✏ Update", fg_color="#A2D2FF",
                                           hover_color="#BDE0FE",
                                           text_color="#4A4E69", command=self.update_fee)
        self.update_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # ---------------------- GENERATE INVOICE TAB ------------------------------------------------------------------------------
        invoice_grid = ctk.CTkFrame(self.invoice_tab, fg_color="#EDE7F6", corner_radius=15)
        invoice_grid.pack(pady=5, padx=10, fill="both", expand=True)

        self.invoice_label = ctk.CTkLabel(invoice_grid, text="Select a record and generate an invoice",
                                          font=("Arial", 12), text_color="#4A4E69")
        self.invoice_label.pack(pady=5)

        self.generate_invoice_button = ctk.CTkButton(invoice_grid, text="📄 Generate Invoice",
                                                     fg_color="#A2D2FF", hover_color="#BDE0FE", text_color="#4A4E69",
                                                     command=self.generate_invoice)
        self.generate_invoice_button.pack(pady=5)

        self.populate_tree()

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

    def load_users(self):
        """Refreshes the user list and updates the tree view."""
        self.populate_tree()  # Refresh fee records in the tree view
        self.update_parent_combobox()  # Refresh parent combobox

    def add_fee(self):
        """Adds a new fee record, ensuring no duplicate Fee Record ID."""
        fee_id = self.fee_id_entry.get().strip()
        amount = self.amount_entry.get().strip()
        status = self.status_var.get()
        parent_name = self.parent_id_box.get().strip()

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

        if parent_name == "Select Parent":
            messagebox.showerror("Error", "Please select a Parent.")
            return

        # Fetch parent_id from the database using the selected parent name
        conn = sqlite3.connect("CeriaPay.db")
        cursor = conn.cursor()
        cursor.execute("SELECT parent_id FROM parent WHERE parent_name = ?", (parent_name,))
        parent_id = cursor.fetchone()
        if not parent_id:
            messagebox.showerror("Error", "Selected parent does not exist.")
            conn.close()
            return
        parent_id = parent_id[0]  # Extract the parent_id

        # Check for duplicate Fee Record ID
        cursor.execute("SELECT COUNT(*) FROM feerecord WHERE feerecord_id = ?", (fee_id,))
        result = cursor.fetchone()[0]

        if result > 0:
            messagebox.showerror("Error", "Cannot enter duplicate Fee Record ID. Please use a unique ID.")
            conn.close()
            return

        # Insert into database
        try:
            cursor.execute("""
                INSERT INTO feerecord (feerecord_id, parent_id, feerecord_amount, feerecord_status, feerecord_duedate, feerecord_timecreated)
                VALUES (?, ?, ?, ?, DATE('now', '+7 days'), datetime('now', 'localtime'))
            """, (fee_id, parent_id, amount, status))
            conn.commit()
            self.populate_tree()  # Refresh table
            self.update_parent_combobox()  # Update parent combobox
            messagebox.showinfo("Success", "Fee record added successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Database error: {e}")
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
        self.update_parent_combobox()  # Refresh parent combobox
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

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 title="Save Invoice As",
                                                 initialfile=f"Invoice_{values[0]}.pdf")

        if file_path:
            c = canvas.Canvas(file_path, pagesize=letter)
            c.setFont("Helvetica-Bold", 20)
            c.drawString(200, 750, "INVOICE")
            c.setFont("Helvetica", 14)

            c.drawString(100, 700, f"Invoice ID: {values[0]}")
            c.drawString(100, 670, f"Parent Name: {values[1]}")
            c.drawString(100, 640, f"Due Date: {values[2]}")
            c.drawString(100, 610, f"Amount: RM{values[3]}")
            c.drawString(100, 580, f"Status: {values[4]}")
            c.drawString(100, 550, f"Created Time: {values[5]}")

            c.drawString(100, 500, "Thank you for your payment!")
            c.save()

            messagebox.showinfo("Success", "Invoice generated successfully!")
