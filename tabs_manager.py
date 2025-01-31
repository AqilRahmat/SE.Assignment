#this file is only used to switch between the tabs inside the program.
#if you do edit this file, please make sure everything works before committing
from tabs.accountant import Account
from tabs.admin import Admin
from tabs.login import Login
from tabs.parent import Parent
from tabs.registration import Register


class FrameManager:
    def __init__(self, root):
        self.root = root
        self.frames = {
            "Login": Login(self.root, self),
            "Admin": Admin(self.root, self),
            "Parent" : Parent(self.root, self),
            "Account" : Account(self.root, self),
            "Register" : Register(self.root, self),
        }

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill="both", expand=True)