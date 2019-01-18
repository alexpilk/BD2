import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
# from .register_pracownik import RegisterPrac


class ItemAddPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.descr_label = tk.Label(self)
        self.opis = tk.StringVar(self)
        self.descr_list = tk.OptionMenu(self, self.opis, "łyżwy", "narty")

        self.size_label = tk.Label(self)
        self.size_input = tk.Entry(self)

        self.status_label = tk.Label(self)
        self.status = tk.StringVar(self)
        self.status_list = tk.OptionMenu(self, self.status, "Wolny", "Zajęty")

        self.add_descr_button = tk.Button(self, text="Dodaj nowy opis sprzętu", command=self.add_desription)
        self.add_button = tk.Button(self, text="Dodaj nowy sprzęt", command=self.add_item)
        self.return_button = tk.Button(self, text="Wróć do strony pracownika", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego sprzętu:")
        self.descr_label.config(text="Rodzaj sprzętu:")
        self.size_label.config(text="Rozmiar:")
        self.status_label.config(text="Status:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')
        self.add_descr_button.config(bg='ghost white')

        self.descr_label.pack()
        self.descr_list.pack()
        self.size_label.pack()
        self.size_input.pack()
        self.status_label.pack()
        self.status_list.pack()
        self.add_descr_button.pack()
        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_item(self):
        description = self.opis.get()
        size = self.size_input.get()
        status = self.status.get()

        if not description or not status or not size:
            messagebox.showinfo('Error', 'Podaj opis, rozmiar i status!')
            return
        messagebox.showinfo('Info', 'Tego jeszcze nie ma ;)')

    def add_desription(self):
        self.controller.show_frame(frames.AddItemDescription)


    def tohome(self):
        self.controller.show_frame(frames.PracownikPage)

