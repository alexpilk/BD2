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

        self.menubar = tk.Menu(self.controller)
        self.infomenu = tk.Menu(self.menubar, tearoff=0)
        self.infomenu.add_command(label="Zmień swoje dane", command=self.change_info)
        self.menubar.add_cascade(label="Info", menu=self.infomenu)
        self.menubar.add_command(label="O programie", command=self.program_info)
        self.menubar.add_command(label="Wyloguj", command=self.logout)

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie klienta, {self.controller.user_data['imie']}")
        self.reserve_item_button.config(bg='ghost white')
        self.reserve_apartment_button.config(bg='ghost white')

        self.controller.config(menu=self.menubar)

        self.reserve_apartment_button.pack()
        self.reserve_item_button.pack()
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

    def program_info(self):
        messagebox.showinfo('Informacje o programie', self.controller.info_o_programie)
