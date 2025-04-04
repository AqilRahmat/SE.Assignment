import sqlite3

import customtkinter as ctk
import database
from dbfunction import update_overdue_status
from tabs_manager import FrameManager

#create the tables
database.create_table()

class MyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('1280x720')
        self.title("CeriaPay")
        self.resizable(width=True, height=True)

        self.frame_manager = FrameManager(self)
        self.frame_manager.show_frame("Testing")

        update_overdue_status()

if __name__ == "__main__":
    app = MyApp()
    app.mainloop()
