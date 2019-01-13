import tkinter as tk
from .base import BaseFrame


class KlientPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie klienta, {self.controller.user_data['imie']}")
        super().tkraise()
