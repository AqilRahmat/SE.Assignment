import customtkinter as ctk
from PIL import ImageTk, Image


def parent_nav(self):
    navbar = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#EDE7F6")
    navbar.pack(fill='x', side="top", padx=0, pady=0)

    logo_image = Image.open('Img/CeriaPay_Logo.png')
    logo_image = logo_image.resize((100, 50))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_button = ctk.CTkButton(navbar, image=logo_image, text="", bg_color="transparent", fg_color="transparent", width=60, height=60, hover=False, hover_color=None)
    logo_button.pack(side="left", padx=10, pady=10)

    logo_button.image = logo_image

    button_frame = ctk.CTkFrame(navbar, fg_color="#EDE7F6")
    button_frame.pack(side="right", padx=20)

    contact_button = ctk.CTkButton(button_frame, text="Contact",
                                   command=lambda: contact_window(),
                                   width=120, height=40, corner_radius=8,
                                   hover_color="#BDE0FE", fg_color="#A2D2FF",
                                   text_color="#4A4E69", font=("Arial", 12, "bold"))
    contact_button.pack(side="left", padx=5, pady=5)

    profile_button = ctk.CTkButton(button_frame, text="Profile",
                                   command=lambda: self.profile_window(),
                                   width=120, height=40, corner_radius=8,
                                   hover_color="#BDE0FE", fg_color="#A2D2FF",
                                   text_color="#4A4E69", font=("Arial", 12, "bold"))
    profile_button.pack(side="left", padx=5, pady=5)

    logout_button = ctk.CTkButton(button_frame, text="Logout",
                                  command=lambda: self.controller.show_frame("Testing"),
                                  width=120, height=40, corner_radius=8,
                                  hover_color="#FF8AB3", fg_color="#FFAFCC",
                                  text_color="#4A4E69", font=("Arial", 12, "bold"))
    logout_button.pack(side="left", padx=5, pady=5)


def nav(self):
    navbar = ctk.CTkFrame(self, height=60, corner_radius=0, fg_color="#EDE7F6")
    navbar.pack(fill='x', side="top", padx=0, pady=0)

    logo_image = Image.open('Img/CeriaPay_Logo.png')
    logo_image = logo_image.resize((100, 50))
    logo_image = ImageTk.PhotoImage(logo_image)

    logo_button = ctk.CTkButton(navbar, image=logo_image, text="", bg_color="transparent", fg_color="transparent", width=60, height=60, hover=False, hover_color=None)
    logo_button.pack(side="left", padx=10, pady=10)

    logo_button.image = logo_image

    button_frame = ctk.CTkFrame(navbar, fg_color="#EDE7F6")
    button_frame.pack(side="right", padx=20)

    contact_button = ctk.CTkButton(button_frame, text="Contact",
                                   command=lambda: contact_window(),
                                   width=120, height=40, corner_radius=8,
                                   hover_color="#BDE0FE", fg_color="#A2D2FF",
                                   text_color="#4A4E69", font=("Arial", 12, "bold"))
    contact_button.pack(side="left", padx=5, pady=5)

    logout_button = ctk.CTkButton(button_frame, text="Logout",
                                  command=lambda: self.controller.show_frame("Testing"),
                                  width=120, height=40, corner_radius=8,
                                  hover_color="#FF8AB3", fg_color="#FFAFCC",
                                  text_color="#4A4E69", font=("Arial", 12, "bold"))
    logout_button.pack(side="left", padx=5, pady=5)


def contact_window():
    contact = ctk.CTkToplevel()
    contact.attributes("-topmost", True)

    contact.title("Contact Us")
    contact.geometry("300x200")

    label = ctk.CTkLabel(contact, text="Contact Us", font=("Arial", 18, "bold"))
    label.pack(pady=(20, 10))

    email_label = ctk.CTkLabel(contact, text="Email: \n CeriaPay@gmail.com", font=("Arial", 12))
    email_label.pack(padx=10, pady=5)

    phone_label = ctk.CTkLabel(contact, text="Phone Number: \n 0123456789", font=("Arial", 12))
    phone_label.pack(padx=10, pady=5)
