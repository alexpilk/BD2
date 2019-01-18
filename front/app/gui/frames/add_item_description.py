import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames


# from .register_pracownik import RegisterPrac


class AddItemDescription(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.add_button = tk.Button(self, text="Dodaj opis", command=self.add_desc)
        self.return_button = tk.Button(self, text="Wróć do dodawania sprzętu", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego opisu sprzętu:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')

        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_desc(self):
        messagebox.showinfo('Info', 'Tego jeszcze nie ma ;)')

    def tohome(self):
        self.controller.show_frame(frames.ItemAddPage)

