#this file is used to switch between the tabs inside the program
from tabs.accountant import Account
from tabs.admin import Admin
from tabs.login import Login
from tabs.parent import Parent
from tabs.teacher import Teacher


class FrameManager:
    def __init__(self, root):
        self.root = root
        self.frames = {
            "Login": Login(self.root, self),
            "Admin": Admin(self.root, self),
            "Teacher" : Teacher(self.root, self),
            "Parent" : Parent(self.root, self),
            "Account" : Account(self.root, self),
        }

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)