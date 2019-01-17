import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames


class PracownikPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.add_button = tk.Button(self, text="Dodaj pracownika", command=self.addworker)
        self.add_client_button = tk.Button(self, text="Dodaj klienta", command=self.addclient)
        self.add_apartment_button = tk.Button(self, text="Dodaj apartament", command=self.addapartment)
        self.logout_button = tk.Button(self, text="Wyloguj", command=self.logout)

    def tkraise(self, *args, **kwargs):
        self.label.config(text=f"Witamy na stronie pracownika, {self.controller.user_data['imie']}")
        self.add_button.config(bg='ghost white')
        self.add_client_button.config(bg='ghost white')
        self.add_apartment_button.config(bg='ghost white')
        self.logout_button.config(bg='ghost white')
        self.add_button.pack()
        self.add_client_button.pack()
        self.add_apartment_button.pack()
        self.logout_button.pack()
        super().tkraise()

    def addworker(self):
        self.controller.show_frame(frames.RegisterPrac)

    def logout(self):
        self.controller.show_frame(frames.LoginPage)

    def addclient(self):
        self.controller.show_frame(frames.RegisterKli)

    def addapartment(self):
        self.controller.show_frame(frames.ApartmentAddPage)
