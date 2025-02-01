#TODO: for testing purpose

import sys

import customtkinter as ctk

class Testing(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Testing")
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Login",
                               command=lambda: self.controller.show_frame("Login"))
        button.pack(pady=10)

        button = ctk.CTkButton(self, text="Admin",
                               command=lambda: self.controller.show_frame("Admin"))
        button.pack(pady=10)

        button = ctk.CTkButton(self, text="Registration",
                               command=lambda: self.controller.show_frame("Register"))
        button.pack(pady=10)

        button = ctk.CTkButton(self, text="Parent",
                               command=lambda: self.controller.show_frame("Parent"))
        button.pack(pady=10)

        button = ctk.CTkButton(self, text="Account",
                               command=lambda: self.controller.show_frame("Account"))
        button.pack(pady=10)

        button = ctk.CTkButton(self, text="Exit",
                               command=lambda: sys.exit(0))
        button.pack(pady=10)