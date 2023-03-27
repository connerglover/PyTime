import customtkinter as ctk
from customtkinter.windows.widgets.scaling import ScalingTracker
from typing import Optional, Tuple, Union


class AlertTopLevel(ctk.CTkToplevel):
    def __init__(
        self,
        *args,
        title: str,
        text: str,
        button_text: str = "Close",
        width: int = 350,
        height: int = 100,
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        **kwargs,
    ):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        # Configure title
        self.title(title)

        # Configure window size and location
        window_scaling = ScalingTracker.get_widget_scaling(self)
        x = int(self.winfo_screenwidth() / 2 * window_scaling - width / 2)
        y = int(self.winfo_screenwidth() / 2 * window_scaling - height / 2)
        self.geometry(
            f"{int(width / window_scaling)}x{int(height / window_scaling)}+{x}+{y}"
        )
        self.resizable(False, False)

        # Configure grid
        self.grid_rowconfigure([0], weight=1)
        self.grid_columnconfigure([0], weight=1)

        # Message
        self.message_label = ctk.CTkLabel(self, font=("", 18), text=text)
        self.message_label.grid(
            row=0, column=0, padx=(10, 10), pady=(10, 0), sticky="nswe"
        )

        # Close Button
        self.close_button = ctk.CTkButton(self, text=button_text, command=self.destroy)
        self.close_button.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))

        # Prevent use of app while activate window is open
        self.grab_set()
