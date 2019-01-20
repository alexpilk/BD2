import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
from app.api import api

class ApartmentAddPage(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.descriptions_get = []
        self.descriptions_get = api.get(
            'OpisApartamentu',
            fields={
                "IdApartamentu": ['id'],
                "OpisApartamentu": ['verbose_name']
            }
        )

        self.elements = []
        for i in range(len(self.descriptions_get)):
            self.elements.append(self.descriptions_get[i]['verbose_name'])

        self.descr_label = tk.Label(self)
        self.opis = tk.StringVar(self)
        self.descr_list = tk.OptionMenu(self, self.opis, *self.elements)
        self.status_label = tk.Label(self)
        self.status = tk.StringVar(self)
        self.status_list = tk.OptionMenu(self, self.status, "Wolny", "Zajęty")

        self.add_button = tk.Button(self, text="Dodaj nowy apartament", command=self.add_ap)
        self.return_button = tk.Button(self, text="Wróć do strony pracownika", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego apartamentu:")
        self.descr_label.config(text="Rodzaj apartamentu:")
        self.status_label.config(text="Status apartamentu:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')

        self.opis.set("---")
        self.status.set("---")

        self.descr_label.pack()
        self.descr_list.pack()
        self.status_label.pack()
        self.status_list.pack()
        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_ap(self):
        description = self.opis.get()
        for item in range(len(self.elements)):
            if self.elements[item] == description:
                description = self.descriptions_get[item]['id']
        status = self.status.get()

        if not description or not status or (status == "---"):
            messagebox.showinfo('Error', 'Podaj opis i status!')
            return

        if status == 'Wolny':
            try:
                apartment = api.create(
                    'Apartament',
                    attributes={
                        "zajety": False
                    },
                    relationships={
                        'opis': {
                            'type': 'OpisApartamentu',
                            'id': description
                        }
                    })
            except Exception:
                messagebox.showinfo('Error', 'Nie można utworzyć wolnego apartamentu!\n'
                                             'Sprawdź czy wszystkie dane zostałyn\n'
                                             'prawidłowo wprowadzone.')
                return
        elif status == 'Zajęty':
            try:
                apartment = api.create(
                    'Apartament',
                    attributes={
                        "zajety": True
                    },
                    relationships={
                        'opis': {
                            'type': 'OpisApartamentu',
                            'id': description
                        }
                    })
            except Exception:
                messagebox.showinfo('Error', 'Nie można utworzyć zajętego apartamentu!\n'
                                             'Sprawdź czy wszystkie dane zostałyn\n'
                                             'prawidłowo wprowadzone.')
                return
        else:
            messagebox.showinfo('Error', 'Nie można utworzyć apartamentu!\n'
                                         'Sprawdź czy wszystkie dane zostały\n'
                                         'prawidłowo wprowadzone.')
            return
        messagebox.showinfo('Info', f'Utworzono nowy: {(apartment["verbose_name"])}.')

    def tohome(self):
        self.controller.show_frame(frames.PracownikPage)

