import customtkinter as ctk
import tkinter as tk


class Menu:
    def __init__(self, master: ctk.CTk | ctk.CTkToplevel):
        self.master = master

        self.menu_font = ("", 12)
        self.menu_bar = tk.Menu(
            master=self.master,
        )

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.file_menu.add_command(
            label="Clear Times",
            underline=0,
            font=self.menu_font,
        )

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Exit", 
            underline=1, 
            font=self.menu_font)
        self.menu_bar.add_cascade(
            label="File", menu=self.file_menu, underline=0, font=self.menu_font
        )

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.edit_menu.add_command(
            label="Copy Mod Message",
            underline=0,
            font=self.menu_font,
        )

        self.edit_menu.add_separator()

        self.edit_menu.add_command(
            label="Settings",
            underline=1,
            font=self.menu_font,
        )
        self.menu_bar.add_cascade(
            label="Edit", menu=self.edit_menu, underline=0, font=self.menu_font
        )

        # Bind menu to app
        self.master.configure(menu=self.menu_bar)