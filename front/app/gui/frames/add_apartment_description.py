import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
# from .register_pracownik import RegisterPrac


class AddApartmentDescription(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.location_label = tk.Label(self)
        self.location = tk.StringVar(self)
        self.location_list = tk.OptionMenu(self, self.location, "Wichrowe Wzgórze", "Ulica Sezamkowa",
                                       "Aleja Gwiazd")

        self.add_button = tk.Button(self, text="Dodaj nowy opis", command=self.add_descr)
        self.return_button = tk.Button(self, text="Wróć do dodawania apartamentu", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego opisu apartamentu:")
        self.location_label.config(text="Lokalizacja:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')

        self.location_label.pack()
        self.location_list.pack()
        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_descr(self):
        location = self.location.get()

        if not location:
            messagebox.showinfo('Error', 'Podaj lokalizacje!')
            return
        messagebox.showinfo('Info', 'Tego jeszcze nie ma ;)')

    def tohome(self):
        self.controller.show_frame(frames.ApartmentAddPage)

