import customtkinter as ctk

class Account(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Account Frame")
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="Exit",
                               command=lambda: self.controller.show_frame("Login"))
        button.pack(pady=10)