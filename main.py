import customtkinter as ctk
from tabs_manager import FrameManager

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title("Multi-Frame App")

        self.frame_manager = FrameManager(self)
        self.frame_manager.show_frame("Login")

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
