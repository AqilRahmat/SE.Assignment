import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

import dbfunction


class Register(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Load images
        side_img_data = Image.open("Img/side-img.png")
        side_img = ctk.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(896, 720))

        # Left Side Image
        ctk.CTkLabel(self, text="", image=side_img, width=896, height=720).place(x=0, y=0)

        self.register_new_account()

    def register_new_account(self):
        name_icon = Image.open("Img/name_icon.png")
        ic_icon = Image.open("Img/ic_icon.png")
        username_icon = Image.open("Img/username_icon.png")
        password_icon = Image.open("Img/password-icon.png")
        phone_icon = Image.open("Img/phone_icon.png")

        name_icon = ctk.CTkImage(dark_image=name_icon, light_image=name_icon, size=(20, 20))
        ic_icon = ctk.CTkImage(dark_image=ic_icon, light_image=ic_icon, size=(20, 20))
        username_icon = ctk.CTkImage(dark_image=username_icon, light_image=username_icon, size=(20, 20))
        password_icon = ctk.CTkImage(dark_image=password_icon, light_image=password_icon, size=(20, 20))
        phone_icon = ctk.CTkImage(dark_image=phone_icon, light_image=phone_icon, size=(20, 20))

        # Right Side Register Frame
        register_frame = ctk.CTkFrame(self, fg_color="#F8F9FA", width=384, height=720)  # Soft Gray Background
        register_frame.place(x=896, y=0)

        # Title Label
        ctk.CTkLabel(register_frame, text="CeriaPay", text_color="#4A4E69", font=("Arial Bold", 24)).place(relx=0.5, y=50, anchor="center")
        ctk.CTkLabel(register_frame, text="Insert Account Credentials", text_color="#7E7E7E", font=("Arial Bold", 12)).place(relx=0.5, y=85, anchor="center")

        # Name Input
        ctk.CTkLabel(register_frame, text="  Name", text_color="#4A4E69", font=("Arial Bold", 14), image=name_icon, compound="left").place(relx=0.5, y=150, anchor="center")
        self.nameinput_field = ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#4A4E69", border_width=1, text_color="#000000")
        self.nameinput_field.place(relx=0.5, y=180, anchor="center")

        # IC Input
        ctk.CTkLabel(register_frame, text="  I/C", text_color="#4A4E69", font=("Arial Bold", 14), image=ic_icon, compound="left").place(relx=0.5, y=230, anchor="center")
        self.icinput_field = ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#4A4E69", border_width=1, text_color="#000000")
        self.icinput_field.place(relx=0.5, y=260, anchor="center")

        # Username Input
        ctk.CTkLabel(register_frame, text="  Username", text_color="#4A4E69", font=("Arial Bold", 14), image=username_icon, compound="left").place(relx=0.5, y=310, anchor="center")
        self.usernameinput_field = ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#4A4E69", border_width=1, text_color="#000000")
        self.usernameinput_field.place(relx=0.5, y=340, anchor="center")

        # Password Input
        ctk.CTkLabel(register_frame, text="  Password", text_color="#4A4E69", font=("Arial Bold", 14), image=password_icon, compound="left").place(relx=0.5, y=390, anchor="center")
        self.password_field = ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#4A4E69", border_width=1, text_color="#000000", show="*")
        self.password_field.place(relx=0.5, y=420, anchor="center")

        # Phone Number Input
        ctk.CTkLabel(register_frame, text="  Phone Number", text_color="#4A4E69", font=("Arial Bold", 14), image=phone_icon, compound="left").place(relx=0.5, y=470, anchor="center")
        self.phoneinput_field = ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#4A4E69", border_width=1, text_color="#000000")
        self.phoneinput_field.place(relx=0.5, y=500, anchor="center")

        # Register Button
        ctk.CTkButton(register_frame, text="Register", fg_color="#A2D2FF", hover_color="#BDE0FE", font=("Arial Bold", 12), text_color="#4A4E69", width=225, command=lambda: self.validate_inserted()).place(relx=0.5, y=560, anchor="center")

        # Exit Button
        ctk.CTkButton(register_frame, text="Exit", command=lambda: self.controller.show_frame("Login"), fg_color="#FCE4EC", hover_color="#FF8AB3", font=("Arial Bold", 9), text_color="#4A4E69", width=225).place(relx=0.5, y=600, anchor="center")

    # Insert user into database
    def insert_new_user(self):
        dbfunction.insert_into_parentdatabase(self.icinput_field.get(), self.nameinput_field.get(), self.phoneinput_field.get(), self.usernameinput_field.get(), self.password_field.get())

    # Registration success/fail popup
    def validate_inserted(self):
        exist = dbfunction.fetch_entry('parent_id', "parent", "parent_id", self.icinput_field.get())

        if self.icinput_field.get() == "" or self.nameinput_field.get() == "" or self.usernameinput_field.get() == "" or self.password_field.get() == "":
            messagebox.showerror("Error", "Please fill all fields")
            return
        if self.icinput_field.get().upper().startswith(("ADM", "ACC")):
            print(self.icinput_field.get())
            messagebox.showerror("ERROR", "Invalid Identification Number")
            self.clear_fields()
            return
        if exist:
            messagebox.showinfo("ERROR", "Registration Failed! This IC number has already been registered. Please Try Again.")
            self.clear_fields()
            return
        else:
            self.insert_new_user()
            messagebox.showinfo("SUCCESS", "Registration Successful!")
            self.clear_fields()

            # Refresh the accountant page
            self.controller.frames["Account"].update_parent_combobox()
            self.controller.show_frame("Login")

    # Clear text fields
    def clear_fields(self):
        self.icinput_field.delete(0, 'end')
        self.nameinput_field.delete(0, 'end')
        self.phoneinput_field.delete(0, 'end')
        self.usernameinput_field.delete(0, 'end')
        self.password_field.delete(0, 'end')
