# TODO: this is only for the customers as the accountant and admin accounts are registered by the admin
import customtkinter as ctk
from PIL import Image

class Register(ctk.CTkFrame):
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
        email_icon_data = Image.open("Img/email-icon.png")
        password_icon_data = Image.open("Img/password-icon.png")
        google_icon_data = Image.open("Img/google-icon.png")

        email_icon = ctk.CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
        password_icon = ctk.CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
        google_icon = ctk.CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

        # Right Side Register Frame
        register_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=384, height=720)
        register_frame.place(x=896, y=0)

        # UI Elements in register_frame (centered)
        ctk.CTkLabel(register_frame, text="CeriaPay", text_color="#601E88",
                     font=("Arial Bold", 24)).place(relx=0.5, y=50, anchor="center")
        ctk.CTkLabel(register_frame, text="Sign in to your account", text_color="#7E7E7E",
                     font=("Arial Bold", 12)).place(relx=0.5, y=85, anchor="center")

        # username Input
        ctk.CTkLabel(register_frame, text="  Username:", text_color="#601E88", font=("Arial Bold", 14),
                     image=email_icon, compound="left").place(relx=0.5, y=150, anchor="center")
        ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                     border_width=1, text_color="#000000").place(relx=0.5, y=180, anchor="center")

        # Password Input
        ctk.CTkLabel(register_frame, text="  Password:", text_color="#601E88", font=("Arial Bold", 14),
                     image=password_icon, compound="left").place(relx=0.5, y=230, anchor="center")
        ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                     border_width=1, text_color="#000000", show="*").place(relx=0.5, y=260, anchor="center")

        # Login Button
        ctk.CTkButton(register_frame, text="Login", fg_color="#601E88", hover_color="#E44982",
                      font=("Arial Bold", 12), text_color="#ffffff", width=225).place(relx=0.5, y=320, anchor="center")

        # Google Login Button
        ctk.CTkButton(register_frame, text="Register New Account", command=lambda: self.register_new_account(), fg_color="#EEEEEE", hover_color="#E44982",
                      font=("Arial Bold", 9), text_color="#601E88", width=225).place(relx=0.5, y=370, anchor="center")

    def register_new_account(self):
        email_icon_data = Image.open("Img/email-icon.png")
        password_icon_data = Image.open("Img/password-icon.png")
        google_icon_data = Image.open("Img/google-icon.png")

        email_icon = ctk.CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
        password_icon = ctk.CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17, 17))
        google_icon = ctk.CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17, 17))

        # Right Side Register Frame
        register_frame = ctk.CTkFrame(self, fg_color="#ffffff", width=384, height=720)
        register_frame.place(x=896, y=0)

        # UI Elements in register_frame (centered)
        ctk.CTkLabel(register_frame, text="CeriaPay", text_color="#601E88",
                     font=("Arial Bold", 24)).place(relx=0.5, y=50, anchor="center")
        ctk.CTkLabel(register_frame, text="Insert Account Credentials", text_color="#7E7E7E",
                     font=("Arial Bold", 12)).place(relx=0.5, y=85, anchor="center")

        # username Input
        ctk.CTkLabel(register_frame, text="  Username:", text_color="#601E88", font=("Arial Bold", 14),
                     image=email_icon, compound="left").place(relx=0.5, y=150, anchor="center")
        ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                     border_width=1, text_color="#000000").place(relx=0.5, y=180, anchor="center")

        # Password Input
        ctk.CTkLabel(register_frame, text="  Password:", text_color="#601E88", font=("Arial Bold", 14),
                     image=password_icon, compound="left").place(relx=0.5, y=230, anchor="center")
        ctk.CTkEntry(register_frame, width=225, fg_color="#EEEEEE", border_color="#601E88",
                     border_width=1, text_color="#000000", show="*").place(relx=0.5, y=260, anchor="center")

        # Login Button
        ctk.CTkButton(register_frame, text="Login", fg_color="#601E88", hover_color="#E44982",
                      font=("Arial Bold", 12), text_color="#ffffff", width=225).place(relx=0.5, y=320, anchor="center")

        # Exit
        ctk.CTkButton(register_frame, text="Exit", command=lambda: self.login_frame(), fg_color="#EEEEEE", hover_color="#E44982",
                      font=("Arial Bold", 9), text_color="#601E88", width=225).place(relx=0.5, y=370, anchor="center")