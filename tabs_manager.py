#this file is only used to switch between the tabs inside the program.
#if you do edit this file, please make sure everything works before committing
from dbfunction import update_overdue_status
from tabs.accountant import Account
from tabs.admin import Admin
from tabs.login import Login
from tabs.parent import Parent
from tabs.registration import Register
from tabs.testing import Testing


class FrameManager:
    def __init__(self, root):
        self.root = root
        self.frames = {
            "Login": Login(self.root, self),
            "Admin": Admin(self.root, self),
            "Parent" : Parent(self.root, self),
            "Account" : Account(self.root, self),
            "Register" : Register(self.root, self),
            "Testing" : Testing(self.root, self),
        }

    def show_frame(self, name):
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Show the selected frame
        frame_to_show = self.frames[name]
        frame_to_show.pack(fill="both", expand=True)

        update_overdue_status()

        # Call populate_parent_tree only if the Parent frame is being shown
        if name == "Parent":
            frame_to_show.create_frame_for_parent()
        if name == "Account":
            frame_to_show.populate_tree()