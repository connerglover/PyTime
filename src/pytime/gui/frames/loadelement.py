import customtkinter as ctk
from typing import Optional, Tuple, Union

from pytime.gui import app


class LoadElement(ctk.CTkFrame):
    def __init__(
        self,
        master: any,
        time: str,
        width: int = 200,
        height: int = 50,
        corner_radius: Optional[Union[int, str]] = None,
        border_width: Optional[Union[int, str]] = None,
        bg_color: Union[str, Tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        border_color: Optional[Union[str, Tuple[str, str]]] = None,
        background_corner_colors: Union[
            Tuple[Union[str, Tuple[str, str]]], None
        ] = None,
        overwrite_preferred_drawing_method: Union[str, None] = None,
        **kwargs,
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
            **kwargs,
        )

        self.app: app.App = self.master.winfo_toplevel()

        self.time_button = ctk.CTkButton(
            master=self,
            text=time,
            font=("", 36),
            bg_color="#343638",
            corner_radius=5,
            width=410,
            height=50,
        )
        self.time_button.grid(row=0, column=0, sticky="nw")
