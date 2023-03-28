import customtkinter as ctk
import tkinter as tk
from customtkinter.windows.widgets.scaling import ScalingTracker

from pytime.gui.frames.retime import RetimeFrame
from pytime.gui.menu import Menu


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure title
        self.title("PyTime")
        
        # Configure icon
        self.iconbitmap(r"src\pytime\assets\icon.ico")
        
        # Bing menu bar
        self.menu = Menu(self)

        # Configure window size and location
        window_scaling = ScalingTracker.get_widget_scaling(self)
        window_width = 800
        window_height = 360
        x = int(self.winfo_screenwidth() / 2 * window_scaling - window_width / 2)
        y = int(self.winfo_screenwidth() / 2 * window_scaling - window_height / 2)
        self.geometry(
            f"{int(window_width / window_scaling)}x{int(window_height / window_scaling)}+{x}+{y}"
        )
        self.resizable(False, False)

        # Configure grid
        self.grid_rowconfigure([0], weight=1)
        self.grid_columnconfigure([0], weight=1)

        # Interface frames
        self.retime_frame = RetimeFrame(self)
        self.retime_frame.grid(row=0, column=0, sticky="nsew")
