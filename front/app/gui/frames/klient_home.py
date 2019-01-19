import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames


class KlientPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)
        self.reserve_apartment_button = tk.Button(self, text="Rezerwuj apartament", command=self.reserve_apartment)
        self.reserve_item_button = tk.Button(self, text="Rezerwuj sprzęt", command=self.reserve_item)
        self.change_button = tk.Button(self, text="Zmien swoje dane", command=self.change_info)
        self.logout_button = tk.Button(self, text="Wyloguj", command=self.logout)

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie klienta, {self.controller.user_data['imie']}")
        self.reserve_item_button.config(bg='ghost white')
        self.reserve_apartment_button.config(bg='ghost white')
        self.change_button.config(bg='ghost white')
        self.logout_button.config(bg='ghost white')

        self.reserve_apartment_button.pack()
        self.reserve_item_button.pack()
        self.change_button.pack()
        self.logout_button.pack()
        super().tkraise()

    def reserve_apartment(self):
        self.controller.show_frame(frames.ApartmentReservePage)

    def reserve_item(self):
        self.controller.show_frame(frames.ItemReservePage)

    def change_info(self):
        self.controller.show_frame(frames.KlientChangePage)

    def logout(self):
        self.controller.set_user(0)
        self.controller.show_frame(frames.LoginPage)

