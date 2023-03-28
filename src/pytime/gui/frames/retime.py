import customtkinter as ctk
from typing import Optional, Tuple, Union
from pytime.gui import app
from pytime.gui.frames.loadviewer import LoadViewerFrame


class RetimeFrame(ctk.CTkFrame):
    def __init__(
        self,
        master: any,
        width: int = 200,
        height: int = 200,
        corner_radius: Optional[Union[int, str]] = 0,
        border_width: Optional[Union[int, str]] = None,
        bg_color: Union[str, Tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        border_color: Optional[Union[str, Tuple[str, str]]] = None,
        background_corner_colors: Union[
            Tuple[Union[str, Tuple[str, str]]], None
        ] = None,
        overwrite_preferred_drawing_method: Union[str, None] = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            background_corner_colors,
            overwrite_preferred_drawing_method,
            **kwargs
        )

        self.app: app.App = self.master.winfo_toplevel()

        # FPS entry box
        self.fps_entry = ctk.CTkEntry(
            master=self, placeholder_text="FPS", width=350, height=50
        )
        self.fps_entry.grid(
            row=0, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky="n"
        )

        # Start time entry box
        self.start_time_entry = ctk.CTkEntry(
            master=self, placeholder_text="Start Time", width=350, height=50
        )
        self.start_time_entry.grid(
            row=1, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky="n"
        )

        # End time entry box
        self.end_time_entry = ctk.CTkEntry(
            master=self, placeholder_text="End Time", width=350, height=50
        )
        self.end_time_entry.grid(
            row=2, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky="n"
        )

        # Add and remove button
        self.add = ctk.CTkButton(master=self, text="Add", width=170, height=50)
        self.add.grid(row=3, column=0, pady=(5, 5), padx=(5, 5), sticky="nw")

        self.remove = ctk.CTkButton(master=self, text="Remove", width=170, height=50)
        self.remove.grid(row=3, column=1, pady=(5, 0), padx=(0, 0), sticky="nw")

        # Start time entry box
        self.start_time_entry = ctk.CTkEntry(
            master=self, placeholder_text="Start Time (Loads)", width=350, height=50
        )
        self.start_time_entry.grid(
            row=4, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky="n"
        )

        # End time entry box
        self.end_time_entry = ctk.CTkEntry(
            master=self, placeholder_text="End Time (Loads)", width=350, height=50
        )
        self.end_time_entry.grid(
            row=5, column=0, columnspan=2, pady=(5, 5), padx=(5, 5), sticky="n"
        )

        # Load viewer frame
        self.loadviewer_frame = LoadViewerFrame(self)
        self.loadviewer_frame.grid(
            row=0,
            column=2,
            columnspan=2,
            rowspan=5,
            pady=(5, 5),
            padx=(5, 5),
            sticky="nse",
        )

        # Time display box
        self.time_display = ctk.CTkLabel(
            master=self,
            bg_color="#333333",
            corner_radius=5,
            font=("", 43.5),
            justify="center",
            width=431,
            height=20,
            text="",
        )
        self.time_display.grid(
            row=5, column=2, columnspan=2, pady=(5, 5), padx=(5, 5), sticky="ne"
        )
