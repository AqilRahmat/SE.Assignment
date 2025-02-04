import customtkinter as ctk
import sqlite3
import dbfunction
import navbar
from tkinter import StringVar

class Admin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg_color='#F8F9FA')
        self.controller = controller

        # Set light appearance mode
        ctk.set_appearance_mode("light")

        self._bg_color='#F8F9FA'
        self.configure(fg_color=self._bg_color)

        self.admin_frame = ctk.CTkFrame(self, bg_color='#F8F9FA')

        # Navbar
        navbar.nav(self)

        # Admin Frame Label
        label = ctk.CTkLabel(self, text="Admin Page", font=("Arial", 18, "bold"), text_color="#4A4E69")
        label.pack(pady=(10, 5))

        # Tab View
        self.tabview = ctk.CTkTabview(self, text_color='black',fg_color="#F8F9FA",
                                      segmented_button_selected_color="#A2D2FF",
                                      segmented_button_selected_hover_color="#BDE0FE",
                                      segmented_button_fg_color='#FFAFCC',
                                      segmented_button_unselected_color="#FFAFCC",
                                      segmented_button_unselected_hover_color="#FF8AB3")
        self.tabview.pack(expand=False, padx=10, pady=5, fill="both")

        # Tabs
        self.add_user_tab = self.tabview.add("Add User")
        self.remove_user_tab = self.tabview.add("Remove User")
        self.parents_tab = self.tabview.add("View Parents")

        self.create_add_user_tab()
        self.create_remove_user_tab()
        self.create_parents_tab()

    def create_add_user_tab(self):
        """Tab for Adding a User."""
        ctk.CTkLabel(self.add_user_tab, text="Add New User", font=("Arial", 16, "bold"), text_color="#4A4E69").pack(
            pady=10)

        add_user_frame = ctk.CTkFrame(self.add_user_tab, fg_color="#EDE7F6", corner_radius=15, border_width=1,
                                      border_color="#BDBDBD")
        add_user_frame.pack(fill="x", padx=10, pady=10)

        user_id_entry = ctk.CTkEntry(add_user_frame, placeholder_text="User ID")
        user_id_entry.pack(pady=5)
        user_name_entry = ctk.CTkEntry(add_user_frame, placeholder_text="User Name")
        user_name_entry.pack(pady=5)
        user_contact_entry = ctk.CTkEntry(add_user_frame, placeholder_text="Contact Number")
        user_contact_entry.pack(pady=5)
        user_username_entry = ctk.CTkEntry(add_user_frame, placeholder_text="Username")
        user_username_entry.pack(pady=5)
        user_password_entry = ctk.CTkEntry(add_user_frame, placeholder_text="Password", show="*")
        user_password_entry.pack(pady=5)

        user_type_var = StringVar()
        user_type_combobox = ctk.CTkComboBox(add_user_frame, values=["Admin", "Accountant"], variable=user_type_var)
        user_type_combobox.set("Admin")
        user_type_combobox.pack(pady=5)

        feedback_label = ctk.CTkLabel(add_user_frame, text="", font=("Arial", 12), text_color="#4A4E69")
        feedback_label.pack(pady=5)

        def add_user():
            user_id = user_id_entry.get()
            user_name = user_name_entry.get()
            user_contactnum = user_contact_entry.get()
            user_username = user_username_entry.get()
            user_password = user_password_entry.get()
            user_type = user_type_var.get()

            if not all([user_id, user_name, user_contactnum, user_username, user_password]):
                feedback_label.configure(text="All fields are required!", text_color="red")
                return

            try:
                conn = sqlite3.connect("CeriaPay.db")
                c = conn.cursor()

                if user_type == "Admin":
                    c.execute("SELECT admin_id FROM administrator WHERE admin_id = ?", (user_id,))
                elif user_type == "Accountant":
                    c.execute("SELECT accountant_id FROM accountant WHERE accountant_id = ?", (user_id,))

                if c.fetchone():
                    feedback_label.configure(text=f"{user_type} ID {user_id} already exists!", text_color="red")
                else:
                    if user_type == "Admin":
                        dbfunction.insert_into_admindatabase(user_id, user_name, user_contactnum, user_username, user_password)
                    elif user_type == "Accountant":
                        dbfunction.insert_into_accountantdatabase(user_id, user_name, user_contactnum, user_username, user_password)
                    feedback_label.configure(text="User added successfully!", text_color="green")
                    user_id_entry.delete(0, "end")
                    user_name_entry.delete(0, "end")
                    user_contact_entry.delete(0, "end")
                    user_username_entry.delete(0, "end")
                    user_password_entry.delete(0, "end")

            except Exception as e:
                feedback_label.configure(text=f"Error: {str(e)}", text_color="red")

        ctk.CTkButton(add_user_frame, text="Add User", font=("Arial", 14, "bold"),
                      fg_color="#A2D2FF", hover_color="#BDE0FE", text_color="black",
                      command=add_user).pack(pady=10)

    def create_remove_user_tab(self):
        """Tab for Removing a User."""
        ctk.CTkLabel(self.remove_user_tab, text="Remove User", font=("Arial", 16, "bold"), text_color="#4A4E69").pack(pady=10)

        user_list_frame = ctk.CTkScrollableFrame(self.remove_user_tab, fg_color="#EDE7F6")
        user_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        feedback_label = ctk.CTkLabel(self.remove_user_tab, text="", font=("Arial", 12), text_color="#4A4E69", fg_color="#EDE7F6")
        feedback_label.pack(pady=5)

        def load_users():
            for widget in user_list_frame.winfo_children():
                widget.destroy()

            conn = sqlite3.connect("CeriaPay.db")
            c = conn.cursor()
            c.execute("SELECT admin_id, admin_name FROM administrator")
            admins = c.fetchall()
            c.execute("SELECT accountant_id, accountant_name FROM accountant")
            accountants = c.fetchall()
            conn.close()

            if not admins and not accountants:
                ctk.CTkLabel(user_list_frame, text="No users found", text_color="#4A4E69").pack()
            else:
                for user_id, user_name in admins + accountants:
                    user_frame = ctk.CTkFrame(user_list_frame, fg_color="#EDE7F6", corner_radius=5)
                    user_frame.pack(fill="x", padx=5, pady=5)

                    ctk.CTkLabel(user_frame, text=f"{user_name} ({user_id})", text_color="#4A4E69", fg_color="#EDE7F6").pack(side="left", padx=10)

                    def remove_user(user_id=user_id):
                        dbfunction.remove_entry("administrator" if user_id in [x[0] for x in admins] else "accountant", "admin_id" if user_id in [x[0] for x in admins] else "accountant_id", user_id)
                        feedback_label.configure(text=f"User {user_id} removed!", text_color="green")
                        load_users()

                    ctk.CTkButton(user_frame, text="Remove", fg_color="#FFAFCC", hover_color="#FDCFE8", text_color="black", command=remove_user).pack(side="right", padx=15)

        load_users()

        ctk.CTkButton(self.remove_user_tab, text="Refresh List", font=("Arial", 14, "bold"),
                      fg_color="#A2D2FF", hover_color="#BDE0FE", text_color="black",
                      command=load_users).pack(pady=10)

    def create_parents_tab(self):
        """Tab for viewing parents."""
        ctk.CTkLabel(self.parents_tab, text="Parents Information", font=("Arial", 16, "bold"), text_color="#4A4E69").pack(pady=10)

        # Frame for scrollable panel
        parent_list_frame = ctk.CTkScrollableFrame(self.parents_tab, fg_color="#EDE7F6", border_width=1, border_color="#BDBDBD", corner_radius=15)
        parent_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Header row for the table
        header_frame = ctk.CTkFrame(parent_list_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=5)

        ctk.CTkLabel(header_frame, text="Parent ID", width=100, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(header_frame, text="Parent Name", width=200, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(header_frame, text="Contact Number", width=150, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)
        ctk.CTkLabel(header_frame, text="Username", width=150, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=5)

        # Add a horizontal separator below the header
        separator = ctk.CTkFrame(parent_list_frame, height=2, fg_color="gray")
        separator.pack(fill="x", padx=5, pady=2)


        def load_parents():
            """Fetch and display all parents in the database."""
            # Clear any existing widgets in the scrollable frame
            for widget in parent_list_frame.winfo_children():
                widget.destroy()

            # Recreate the header row
            header_frame = ctk.CTkFrame(parent_list_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=5, pady=2)
            ctk.CTkLabel(header_frame, text="Parent ID", width=100, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
            ctk.CTkLabel(header_frame, text="Parent Name", width=200, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(header_frame, text="Contact Number", width=150, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)
            ctk.CTkLabel(header_frame, text="Username", width=150, anchor="w", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=5)

            # Add a horizontal separator below the header
            separator = ctk.CTkFrame(parent_list_frame, height=2, fg_color="gray")
            separator.pack(fill="x", padx=5, pady=2)

            try:
                # Fetch parent data from the database
                conn = sqlite3.connect("CeriaPay.db")
                c = conn.cursor()
                c.execute("SELECT parent_id, parent_name, parent_contactnum, parent_username FROM parent")
                parents = c.fetchall()
                conn.close()

                if not parents:
                    ctk.CTkLabel(parent_list_frame, text="No parents found.", font=("Arial", 12)).pack(pady=10)
                else:
                    # Display each parent's details in the scrollable frame
                    for i, (parent_id, parent_name, parent_contactnum, parent_username) in enumerate(parents):
                        row_frame = ctk.CTkFrame(parent_list_frame, fg_color="transparent", corner_radius=5)
                        row_frame.pack(fill="x", padx=5, pady=2)

                        # Display parent details in columns
                        ctk.CTkLabel(row_frame, text=parent_id, width=100, anchor="w", font=("Arial", 11)).grid(row=0, column=0, padx=5)
                        ctk.CTkLabel(row_frame, text=parent_name, width=200, anchor="w", font=("Arial", 11)).grid(row=0, column=1, padx=5)
                        ctk.CTkLabel(row_frame, text=parent_contactnum, width=150, anchor="w", font=("Arial", 11)).grid(row=0, column=2, padx=5)
                        ctk.CTkLabel(row_frame, text=parent_username, width=150, anchor="w", font=("Arial", 11)).grid(row=0, column=3, padx=5)

                        # Add a horizontal separator between rows
                        separator = ctk.CTkFrame(parent_list_frame, height=1, fg_color="lightgray")
                        separator.pack(fill="x", padx=5, pady=2)

            except Exception as e:
                ctk.CTkLabel(parent_list_frame, text=f"Error loading parents: {str(e)}", text_color="red").pack(pady=10)

        # Load parents when the tab is created
        load_parents()

        # Add a refresh button to reload the parent list
        ctk.CTkButton(self.parents_tab, text="Refresh List", font=("Arial", 14, "bold"),
                      fg_color="#A2D2FF", hover_color="#BDE0FE", text_color="black",
                      command=load_parents).pack(pady=10)