#TODO: this is only for the customers as the accountant and admin accounts are registered by the admin
#TODO:
import customtkinter as ctk

class Register(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Register Frame")
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Exit",
                               command=lambda: self.controller.show_frame("Login"))
        button.pack(pady=10)
