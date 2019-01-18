import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
# from .register_pracownik import RegisterPrac


class ApartmentAddPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.descr_label = tk.Label(self)
        self.opis = tk.StringVar(self)
        self.descr_list = tk.OptionMenu(self, self.opis, "Namiot gdzieś", "Pokój w Los Angeles",
                                       "Domek Letniskowy na Ulicy sezamkowej", "Pałac w bagnie")
        self.status_label = tk.Label(self)
        self.status = tk.StringVar(self)
        self.status_list = tk.OptionMenu(self, self.status, "Wolny", "Zajęty")

        self.add_descr_button = tk.Button(self, text="Dodaj nowy opis apartamentu", command=self.add_desription)
        self.add_button = tk.Button(self, text="Dodaj nowy apartament", command=self.add_ap)
        self.return_button = tk.Button(self, text="Wróć do strony pracownika", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego apartamentu:")
        self.descr_label.config(text="Rodzaj apartamentu:")
        self.status_label.config(text="Status apartamentu:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')
        self.add_descr_button.config(bg='ghost white')

        self.descr_label.pack()
        self.descr_list.pack()
        self.status_label.pack()
        self.status_list.pack()
        self.add_descr_button.pack()
        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_ap(self):
        description = self.opis.get()
        status = self.status.get()

        if not description or not status:
            messagebox.showinfo('Error', 'Podaj opis, lokalizację i status!')
            return
        messagebox.showinfo('Info', 'Tego jeszcze nie ma ;)')

    def add_desription(self):
        self.controller.show_frame(frames.AddApartmentDescription)


    def tohome(self):
        self.controller.show_frame(frames.PracownikPage)

