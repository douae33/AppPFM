import tkinter as tk
from customtkinter import CTkFrame, CTkButton

class Navbar:
    def __init__(self, root):
        self.root = root
        self.navbar_frame = None

    def render(self, button_configurations):
        if self.navbar_frame:
            self.navbar_frame.destroy()

        self.navbar_frame = CTkFrame(self.root, height=10, corner_radius=0, fg_color="#B0E0E6")
        self.navbar_frame.pack(fill="x", side="top")

        button_container = tk.Frame(self.navbar_frame, bg="#B0E0E6")
        button_container.pack(expand=True, pady=2)

        for label, command in button_configurations:
            button = CTkButton(
                button_container, text=label, command=command,
                fg_color="#8B0000", hover_color="#FFA07A", text_color="white",
                corner_radius=10, font=("Arial", 14, "bold"),
                width=150, height=40
            )
            button.pack(side="left", padx=20, pady=5)
