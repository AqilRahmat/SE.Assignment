import customtkinter as ctk
from PIL import ImageTk, Image


# navigation bar for parent
def parent_nav(self):
    navbar = ctk.CTkFrame(self, height=20)
    navbar.pack(fill='x')

    # Load the logo image using Pillow
    logo_image = Image.open('Img/CeriaPay_Logo.png')  # Replace with your logo path
    logo_image = logo_image.resize((50, 50))  # Resize image as needed
    logo_image = ImageTk.PhotoImage(logo_image)  # Convert to PhotoImage format for tkinter

    # Insert the image into a button
    logo_button = ctk.CTkButton(navbar, image=logo_image, text="", bg_color="transparent", fg_color="transparent")
    logo_button.pack(side="left", padx=5, pady=5)

    # Keep a reference to the image to prevent garbage collection
    logo_button.image = logo_image

    logout_button = ctk.CTkButton(navbar, text="Logout",
                                  command=lambda: self.controller.show_frame("Login"),
                                  width=10,
                                  height=50)
    logout_button.pack(side="right", padx=5, pady=5)

    contact_button = ctk.CTkButton(navbar, text="Contact",
                                   command=lambda: contact_window(),
                                   width=10,
                                   height=50)
    contact_button.pack(side="right", padx=5, pady=5)

    profile_button = ctk.CTkButton(navbar, text="Profile",
                                   command=lambda: self.profile_window(),
                                   width=10,
                                   height=50)
    profile_button.pack(side="right", padx=5, pady=5)

#navbar for the rest
def nav(self):
    navbar = ctk.CTkFrame(self, height=20)
    navbar.pack(fill='x')

    # Load the logo image using Pillow
    logo_image = Image.open('Img/CeriaPay_Logo.png')  # Replace with your logo path
    logo_image = logo_image.resize((50, 50))  # Resize image as needed
    logo_image = ImageTk.PhotoImage(logo_image)  # Convert to PhotoImage format for tkinter

    # Insert the image into a button
    logo_button = ctk.CTkButton(navbar, image=logo_image, text="", bg_color="transparent", fg_color="transparent")
    logo_button.pack(side="left", padx=5, pady=5)

    # Keep a reference to the image to prevent garbage collection
    logo_button.image = logo_image

    logout_button = ctk.CTkButton(navbar, text="Logout",
                                  command=lambda: self.controller.show_frame("Login"),
                                  width=10,
                                  height=50)
    logout_button.pack(side="right", padx=5, pady=5)

    contact_button = ctk.CTkButton(navbar, text="Contact",
                                   command=lambda: contact_window(),
                                   width=10,
                                   height=50)
    contact_button.pack(side="right", padx=5, pady=5)

#popup for contact button
def contact_window():
    contact = ctk.CTkToplevel()
    contact.attributes("-topmost", True)

    contact.title("Contact Us")
    contact.geometry("300x200")

    label = ctk.CTkLabel(contact, text="Contact Us")
    label.pack()

    email_label = ctk.CTkLabel(contact, text="Email: \n CeriaPay@gmail.com")
    email_label.pack(padx=5, pady=5)

    phone_label = ctk.CTkLabel(contact, text="Phone Number: \n 0123456789")
    phone_label.pack(padx=5, pady=5)
