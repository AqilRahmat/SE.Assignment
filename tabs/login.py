import customtkinter as ctk
from tkinter import messagebox
from PIL import (Image,ImageTk)
import dbfunction

class Login(ctk.CTkFrame):
    username_for_profile = None # to be used for the profile tab in parent tab
    phonenum_for_profile = None
    password_for_profile = None
    ic_for_profile = None

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load images
        side_img_data = Image.open("Img/side-img.png")
        side_img = ctk.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(896, 720))

        # Left Side Image
        ctk.CTkLabel(self, text="", image=side_img, width=896, height=720).place(x=0, y=0)

        self.login_frame()

    def login_frame(self):
        ic_icon = Image.open("Img/ic_icon.png")
        password_icon = Image.open("Img/password-icon.png")

        ic_icon = ctk.CTkImage(dark_image=ic_icon, light_image=ic_icon, size=(20, 20))
        password_icon = ctk.CTkImage(dark_image=password_icon, light_image=password_icon, size=(20, 20))

        # Right Side Register Frame
        register_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=384, height=720)
        register_frame.place(x=896, y=0)

        # UI Elements in register_frame (centered)
        ctk.CTkLabel(register_frame, text="CeriaPay", text_color="#601E88",
                     font=("Arial Bold", 24)).place(relx=0.5, y=50, anchor="center")
        ctk.CTkLabel(register_frame, text="Sign in to your account", text_color="#7E7E7E",
                     font=("Arial Bold", 12)).place(relx=0.5, y=85, anchor="center")

        # IC input
        ctk.CTkLabel(register_frame, text="  IC", text_color="#601E88", font=("Arial Bold", 14),
                     image=ic_icon, compound="left").place(relx=0.5, y=150, anchor="center")
        self.icinput_field = ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                                border_width=1, text_color="#000000")
        self.icinput_field.place(relx=0.5, y=180, anchor="center")

        # Password Input
        ctk.CTkLabel(register_frame, text="  Password", text_color="#601E88", font=("Arial Bold", 14),
                     image=password_icon, compound="left").place(relx=0.5, y=230, anchor="center")
        self.password_field = ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                                           border_width=1, text_color="#000000", show="*")
        self.password_field.place(relx=0.5, y=260, anchor="center")

        # Login Button
        ctk.CTkButton(register_frame, text="Login", command=lambda: self.validate_login(), fg_color="#601E88", hover_color="#E44982",
                      font=("Arial Bold", 12), text_color="#ffffff", width=225).place(relx=0.5, y=320, anchor="center")

        # Register button
        ctk.CTkButton(register_frame, text="Register New Account", command=lambda: self.controller.show_frame("Register"),
                      fg_color="#EEEEEE", hover_color="#E44982",
                      font=("Arial Bold", 9), text_color="#601E88", width=225).place(relx=0.5, y=370, anchor="center")

        button = ctk.CTkButton(self, text="Exit",
                               command=lambda: self.controller.show_frame("Testing"))
        button.pack(pady=10)

    def validate_login(self):
        exist_in_admin = dbfunction.fetch_entry('admin_id','administrator', 'admin_id', self.icinput_field.get())
        exist_in_account = dbfunction.fetch_entry('accountant_id', 'accountant', 'accountant_id', self.icinput_field.get())
        exist_in_parent = dbfunction.fetch_entry('parent_id', 'parent', 'parent_id', self.icinput_field.get())

        if exist_in_admin:
            admin_validate = dbfunction.fetch_entry('admin_password', 'administrator', 'admin_id', self.icinput_field.get())
            if admin_validate == self.password_field.get():
                self.controller.show_frame("Admin")
                self.icinput_field.delete(0, 'end')
                self.password_field.delete(0, 'end')
                return
            else:
                messagebox.showerror("ERROR", "Incorrect password. Please Try Again.")
                self.password_field.delete(0, 'end')
                return

        if exist_in_account:
            account_validate = dbfunction.fetch_entry('accountant_password', 'accountant', 'accountant_id', self.icinput_field.get())
            if account_validate == self.password_field.get():
                self.controller.show_frame("Account")
                self.icinput_field.delete(0, 'end')
                self.password_field.delete(0, 'end')
                return
            else:
                messagebox.showerror("ERROR", "Incorrect password. Please Try Again.")
                self.password_field.delete(0, 'end')
                return

        if exist_in_parent:
            parent_validate = dbfunction.fetch_entry('parent_password', 'parent', 'parent_id', self.icinput_field.get())

            Login.ic_for_profile = self.icinput_field.get()
            Login.username_for_profile = dbfunction.fetch_entry('parent_username', 'parent', 'parent_id', self.icinput_field.get())
            Login.phonenum_for_profile = dbfunction.fetch_entry('parent_contactnum', 'parent', 'parent_id',self.icinput_field.get())
            Login.password_for_profile = dbfunction.fetch_entry('parent_password', 'parent', 'parent_id', self.icinput_field.get())

            if self.password_field.get() == parent_validate:
                self.controller.show_frame("Parent")
                self.icinput_field.delete(0, 'end')
                self.password_field.delete(0, 'end')
                return
            else:
                messagebox.showerror("ERROR", "Incorrect password. Please Try Again.")
                self.password_field.delete(0, 'end')
                return

        else:
            messagebox.showerror("ERROR", "User Does Not Exist. Please Register A New Account.")
            self.icinput_field.delete(0, 'end')
            self.password_field.delete(0, 'end')