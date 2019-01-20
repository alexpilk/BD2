import tkinter as tk
from tkinter import messagebox
from .base import BaseFrame
from app.gui import frames
from app.api import api


class AddApartmentDescription(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.label = tk.Label(self)
        self.label.pack(pady=10, padx=10)

        self.type_get = []
        self.type_get = api.get(
            'RodzajApartamentu',
            fields={
                "IdTypu": ['id'],
                "NazwaTypu": ['nazwa']
            }
        )

        self.type_elements = []
        for i in range(len(self.type_get)):
            self.type_elements.append(self.type_get[i]['nazwa'])

        self.type_label = tk.Label(self)
        self.opis1 = tk.StringVar(self)
        self.type_list = tk.OptionMenu(self, self.opis1, *self.type_elements)

        self.locations_get = []
        self.locations_get = api.get(
            'Lokalizacja',
            fields={
                "IdLokacji": ['id'],
                "NazwaLokacji": ['verbose_name']
            }
        )

        self.loc_elements = []
        for i in range(len(self.locations_get)):
            self.loc_elements.append(self.locations_get[i]['verbose_name'])

        self.location_label = tk.Label(self)
        self.opis = tk.StringVar(self)
        self.location_list = tk.OptionMenu(self, self.opis, *self.loc_elements)

        self.price_label = tk.Label(self)
        self.price_input = tk.Entry(self)

        self.add_button = tk.Button(self, text="Dodaj opis", command=self.add_desc)
        self.return_button = tk.Button(self, text="Wróć do strony głównej", command=self.tohome)

    def tkraise(self, *args, **kwargs):
        self.label.config(text="Dodawanie nowego opisu apartamentu:")
        self.type_label.config(text="Typ:")
        self.location_label.config(text="Lokalizacja:")
        self.price_label.config(text="Cena za noc:")
        self.add_button.config(bg='ghost white')
        self.return_button.config(bg='ghost white')

        self.price_input.delete(0, tk.END)
        self.opis.set("---")
        self.opis1.set("---")

        self.type_label.pack()
        self.type_list.pack()
        self.location_label.pack()
        self.location_list.pack()
        self.price_label.pack()
        self.price_input.pack()
        self.add_button.pack()
        self.return_button.pack()
        super().tkraise()

    def add_desc(self):
        price = self.price_input.get()
        aptype = self.opis1.get()
        for item in range(len(self.type_elements)):
            if self.type_elements[item] == aptype:
                aptype = self.type_get[item]['id']

        location = self.opis.get()
        for item in range(len(self.loc_elements)):
            if self.loc_elements[item] == location:
                location = self.locations_get[item]['id']

        if not aptype or not location or not price:
            messagebox.showinfo('Error', 'Podaj rodzaj, lokalizację i cenę!')
            return

        try:
            new_descript = api.create(
                'OpisApartamentu',
                attributes={
                    'cena': price
                },
                relationships={
                    'rodzaj': {
                        'type': 'RodzajApartamentu',
                        'id': aptype
                    },
                    'lokalizacja': {
                        'type': 'Lokalizacja',
                        'id': location
                    }
                })
        except Exception:
            messagebox.showinfo('Error', 'Nie można utworzyć opisu apartamentu! '
                                         'Sprawdź czy wszystkie dane zostały '
                                         'prawidłowo wprowadzone.')
            return
        messagebox.showinfo('Info', f'Utworzono nowy: {(new_descript["verbose_name"])}.')

    def tohome(self):
        self.controller.show_frame(frames.PracownikPage)

