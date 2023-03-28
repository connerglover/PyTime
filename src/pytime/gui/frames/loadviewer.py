import customtkinter as ctk
from customtkinter import CTkFont
from typing import Optional, Tuple, Union, Literal
from pytime.gui import app
from pytime.gui.frames.loadelement import LoadElement


class LoadViewerFrame(ctk.CTkScrollableFrame):
    def __init__(
        self,
        master: any,
        width: int = 410,
        height: int = 200,
        corner_radius: Optional[Union[int, str]] = 5,
        border_width: Optional[Union[int, str]] = None,
        bg_color: Union[str, Tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        border_color: Optional[Union[str, Tuple[str, str]]] = None,
        scrollbar_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        scrollbar_button_color: Optional[Union[str, Tuple[str, str]]] = None,
        scrollbar_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
        label_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        label_text_color: Optional[Union[str, Tuple[str, str]]] = None,
        label_text: str = "",
        label_font: Optional[Union[tuple, CTkFont]] = None,
        label_anchor: str = "center",
        orientation: Literal["vertical", "horizontal"] = "vertical",
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
            scrollbar_fg_color,
            scrollbar_button_color,
            scrollbar_button_hover_color,
            label_fg_color,
            label_text_color,
            label_text,
            label_font,
            label_anchor,
            orientation,
        )
        
        self.app: app.App = self.master.winfo_toplevel()
        