#TODO: Admin can add/remove teacher & accountant account
#TODO: Can view parents information
#TODO: Can view & manage (update payment), view payment history view fee status

import customtkinter as ctk
import navbar

class Admin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        navbar.nav(self)

        label = ctk.CTkLabel(self, text="Admin Frame")
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Exit",
                               command=lambda: self.controller.show_frame("Login"))
        button.pack(pady=10)