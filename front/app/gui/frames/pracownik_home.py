import tkinter as tk
from .base import BaseFrame
# from .register_pracownik import RegisterPage as addprac


class PracownikPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)
        self.button = tk.Button(self, text="Dodaj")#, command=self.addworker)

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie pracownika, {self.controller.user_data['imie']}")
        self.button.config(bg='ghost white')
        self.button.pack()
        super().tkraise()

    def addworker(self):
        # self.controller.show_frame(addprac)
        return
